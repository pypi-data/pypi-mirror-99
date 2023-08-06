# Copyright 2014 OpenStack Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import base64
import collections
import datetime
import json
import logging
import multiprocessing
import os
import psutil
import shutil
import signal
import shlex
import socket
import subprocess
import tempfile
import threading
import time
import traceback
from concurrent.futures.process import ProcessPoolExecutor, BrokenProcessPool
import re

import git
from urllib.parse import urlsplit

from zuul.lib.ansible import AnsibleManager
from zuul.lib.gearworker import ZuulGearWorker
from zuul.lib.result_data import get_warnings_from_result_data
from zuul.lib.yamlutil import yaml
from zuul.lib.config import get_default
from zuul.lib.logutil import get_annotated_logger
from zuul.lib.statsd import get_statsd
from zuul.lib import filecomments

import gear

import zuul.lib.repl
import zuul.merger.merger
import zuul.ansible.logconfig
from zuul.executor.sensors.cpu import CPUSensor
from zuul.executor.sensors.hdd import HDDSensor
from zuul.executor.sensors.pause import PauseSensor
from zuul.executor.sensors.startingbuilds import StartingBuildsSensor
from zuul.executor.sensors.ram import RAMSensor
from zuul.lib import commandsocket
from zuul.merger.server import BaseMergeServer, RepoLocks

BUFFER_LINES_FOR_SYNTAX = 200
COMMANDS = ['stop', 'pause', 'unpause', 'graceful', 'verbose',
            'unverbose', 'keep', 'nokeep', 'repl', 'norepl']
DEFAULT_FINGER_PORT = 7900
DEFAULT_STREAM_PORT = 19885
BLACKLISTED_ANSIBLE_CONNECTION_TYPES = [
    'network_cli', 'kubectl', 'project', 'namespace']
BLACKLISTED_VARS = dict(
    ansible_ssh_executable='ssh',
    ansible_ssh_common_args='-o PermitLocalCommand=no',
    ansible_sftp_extra_args='-o PermitLocalCommand=no',
    ansible_scp_extra_args='-o PermitLocalCommand=no',
    ansible_ssh_extra_args='-o PermitLocalCommand=no',
)


class StopException(Exception):
    """An exception raised when an inner loop is asked to stop."""
    pass


class ExecutorError(Exception):
    """A non-transient run-time executor error

    This class represents error conditions detected by the executor
    when preparing to run a job which we know are consistently fatal.
    Zuul should not reschedule the build in these cases.
    """
    pass


class RoleNotFoundError(ExecutorError):
    pass


class PluginFoundError(ExecutorError):
    pass


class DiskAccountant(object):
    ''' A single thread to periodically run du and monitor a base directory

    Whenever the accountant notices a dir over limit, it will call the
    given func with an argument of the job directory. That function
    should be used to remediate the problem, generally by killing the
    job producing the disk bloat). The function will be called every
    time the problem is noticed, so it should be handled synchronously
    to avoid stacking up calls.
    '''
    log = logging.getLogger("zuul.ExecutorDiskAccountant")

    def __init__(self, jobs_base, limit, func, cache_dir, usage_func=None):
        '''
        :param str jobs_base: absolute path name of dir to be monitored
        :param int limit: maximum number of MB allowed to be in use in any one
                          subdir
        :param callable func: Function to call with overlimit dirs
        :param str cache_dir: absolute path name of dir to be passed as the
                              first argument to du. This will ensure du does
                              not count any hardlinks to files in this
                              directory against a single job.
        :param callable usage_func: Optional function to call with usage
                                    for every dir _NOT_ over limit
        '''
        # Remove any trailing slash to ensure dirname equality tests work
        cache_dir = cache_dir.rstrip('/')
        jobs_base = jobs_base.rstrip('/')
        # Don't cross the streams
        if cache_dir == jobs_base:
            raise Exception("Cache dir and jobs dir cannot be the same")
        self.thread = threading.Thread(target=self._run,
                                       name='diskaccountant')
        self.thread.daemon = True
        self._running = False
        self.jobs_base = jobs_base
        self.limit = limit
        self.func = func
        self.cache_dir = cache_dir
        self.usage_func = usage_func
        self.stop_event = threading.Event()

    def _run(self):
        while self._running:
            # Walk job base
            before = time.time()
            du = subprocess.Popen(
                ['du', '-m', '--max-depth=1', self.cache_dir, self.jobs_base],
                stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
            for line in du.stdout:
                (size, dirname) = line.rstrip().split()
                dirname = dirname.decode('utf8')
                if dirname == self.jobs_base or dirname == self.cache_dir:
                    continue
                if os.path.dirname(dirname) == self.cache_dir:
                    continue
                size = int(size)
                if size > self.limit:
                    self.log.warning(
                        "{job} is using {size}MB (limit={limit})"
                        .format(size=size, job=dirname, limit=self.limit))
                    self.func(dirname)
                elif self.usage_func:
                    self.log.debug(
                        "{job} is using {size}MB (limit={limit})"
                        .format(size=size, job=dirname, limit=self.limit))
                    self.usage_func(dirname, size)
            du.wait()
            du.stdout.close()
            after = time.time()
            # Sleep half as long as that took, or 1s, whichever is longer
            delay_time = max((after - before) / 2, 1.0)
            self.stop_event.wait(delay_time)

    def start(self):
        if self.limit < 0:
            # No need to start if there is no limit.
            return
        self._running = True
        self.thread.start()

    def stop(self):
        if not self.running:
            return
        self._running = False
        self.stop_event.set()
        self.thread.join()

    @property
    def running(self):
        return self._running


class Watchdog(object):
    def __init__(self, timeout, function, args):
        self.timeout = timeout
        self.function = function
        self.args = args
        self.thread = threading.Thread(target=self._run,
                                       name='watchdog')
        self.thread.daemon = True
        self.timed_out = None

        self.end = 0

        self._running = False
        self._stop_event = threading.Event()

    def _run(self):
        while self._running and time.time() < self.end:
            self._stop_event.wait(10)
        if self._running:
            self.timed_out = True
            self.function(*self.args)
        else:
            # Only set timed_out to false if we aren't _running
            # anymore. This means that we stopped running not because
            # of a timeout but because normal execution ended.
            self.timed_out = False

    def start(self):
        self._running = True
        self.end = time.time() + self.timeout
        self.thread.start()

    def stop(self):
        self._running = False
        self._stop_event.set()


class SshAgent(object):

    def __init__(self, zuul_event_id=None, build=None):
        self.env = {}
        self.ssh_agent = None
        self.log = get_annotated_logger(
            logging.getLogger("zuul.ExecutorServer"),
            zuul_event_id, build=build)

    def start(self):
        if self.ssh_agent:
            return
        with open('/dev/null', 'r+') as devnull:
            ssh_agent = subprocess.Popen(['ssh-agent'], close_fds=True,
                                         stdout=subprocess.PIPE,
                                         stderr=devnull,
                                         stdin=devnull)
        (output, _) = ssh_agent.communicate()
        output = output.decode('utf8')
        for line in output.split("\n"):
            if '=' in line:
                line = line.split(";", 1)[0]
                (key, value) = line.split('=')
                self.env[key] = value
        self.log.info('Started SSH Agent, {}'.format(self.env))

    def stop(self):
        if 'SSH_AGENT_PID' in self.env:
            try:
                os.kill(int(self.env['SSH_AGENT_PID']), signal.SIGTERM)
            except OSError:
                self.log.exception(
                    'Problem sending SIGTERM to agent {}'.format(self.env))
            self.log.debug('Sent SIGTERM to SSH Agent, {}'.format(self.env))
            self.env = {}

    def __del__(self):
        try:
            self.stop()
        except Exception:
            self.log.exception('Exception in SshAgent destructor')
        try:
            super().__del__(self)
        except AttributeError:
            pass

    def add(self, key_path):
        env = os.environ.copy()
        env.update(self.env)
        key_path = os.path.expanduser(key_path)
        self.log.debug('Adding SSH Key {}'.format(key_path))
        try:
            subprocess.check_output(['ssh-add', key_path], env=env,
                                    stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            self.log.exception('ssh-add failed. stdout: %s, stderr: %s',
                               e.output, e.stderr)
            raise
        self.log.info('Added SSH Key {}'.format(key_path))

    def addData(self, name, key_data):
        env = os.environ.copy()
        env.update(self.env)
        self.log.debug('Adding SSH Key {}'.format(name))
        try:
            subprocess.check_output(['ssh-add', '-'], env=env,
                                    input=key_data.encode('utf8'),
                                    stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            self.log.exception('ssh-add failed. stdout: %s, stderr: %s',
                               e.output, e.stderr)
            raise
        self.log.info('Added SSH Key {}'.format(name))

    def remove(self, key_path):
        env = os.environ.copy()
        env.update(self.env)
        key_path = os.path.expanduser(key_path)
        self.log.debug('Removing SSH Key {}'.format(key_path))
        subprocess.check_output(['ssh-add', '-d', key_path], env=env,
                                stderr=subprocess.PIPE)
        self.log.info('Removed SSH Key {}'.format(key_path))

    def list(self):
        if 'SSH_AUTH_SOCK' not in self.env:
            return None
        env = os.environ.copy()
        env.update(self.env)
        result = []
        for line in subprocess.Popen(['ssh-add', '-L'], env=env,
                                     stdout=subprocess.PIPE).stdout:
            line = line.decode('utf8')
            if line.strip() == 'The agent has no identities.':
                break
            result.append(line.strip())
        return result


class KubeFwd(object):
    kubectl_command = 'kubectl'

    def __init__(self, zuul_event_id, build, kubeconfig, context,
                 namespace, pod):
        self.port = None
        self.fwd = None
        self.log = get_annotated_logger(
            logging.getLogger("zuul.ExecutorServer"),
            zuul_event_id, build=build)
        self.kubeconfig = kubeconfig
        self.context = context
        self.namespace = namespace
        self.pod = pod

    def start(self):
        if self.fwd:
            return
        with open('/dev/null', 'r+') as devnull:
            fwd = subprocess.Popen(
                [self.kubectl_command, '--kubeconfig=%s' % self.kubeconfig,
                 '--context=%s' % self.context,
                 '-n', self.namespace,
                 'port-forward',
                 'pod/%s' % self.pod, ':19885'],
                close_fds=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                stdin=devnull)
        line = fwd.stdout.readline().decode('utf8')
        m = re.match(r'^Forwarding from 127.0.0.1:(\d+) -> 19885', line)
        if m:
            self.port = m.group(1)
        else:
            try:
                self.log.error("Could not find the forwarded port: %s", line)
                fwd.kill()
            except Exception:
                pass
            raise Exception("Unable to start kubectl port forward")
        self.fwd = fwd
        self.log.info('Started Kubectl port forward on port {}'.format(
            self.port))

    def stop(self):
        try:
            if self.fwd:
                self.fwd.kill()
                self.fwd.wait()

                # clear stdout buffer before its gone to not miss out on
                # potential connection errors
                fwd_stdout = [line.decode('utf8') for line in self.fwd.stdout]
                self.log.debug(
                    "Rest of kubectl port forward output was: %s",
                    "".join(fwd_stdout)
                )

                self.fwd = None
        except Exception:
            self.log.exception('Unable to stop kubectl port-forward:')

    def __del__(self):
        try:
            self.stop()
        except Exception:
            self.log.exception('Exception in KubeFwd destructor')
        try:
            super().__del__(self)
        except AttributeError:
            pass


class JobDirPlaybook(object):
    def __init__(self, root):
        self.root = root
        self.trusted = None
        self.project_canonical_name = None
        self.branch = None
        self.canonical_name_and_path = None
        self.path = None
        self.roles = []
        self.roles_path = []
        self.ansible_config = os.path.join(self.root, 'ansible.cfg')
        self.project_link = os.path.join(self.root, 'project')
        self.secrets_root = os.path.join(self.root, 'secrets')
        os.makedirs(self.secrets_root)
        self.secrets = os.path.join(self.secrets_root, 'secrets.yaml')
        self.secrets_content = None

    def addRole(self):
        count = len(self.roles)
        root = os.path.join(self.root, 'role_%i' % (count,))
        os.makedirs(root)
        self.roles.append(root)
        return root


class JobDir(object):
    def __init__(self, root, keep, build_uuid):
        '''
        :param str root: Root directory for the individual job directories.
            Can be None to use the default system temp root directory.
        :param bool keep: If True, do not delete the job directory.
        :param str build_uuid: The unique build UUID. If supplied, this will
            be used as the temp job directory name. Using this will help the
            log streaming daemon find job logs.
        '''
        # root
        #   ansible (mounted in bwrap read-only)
        #     logging.json
        #     inventory.yaml
        #     extra_vars.yaml
        #     vars_blacklist.yaml
        #   .ansible (mounted in bwrap read-write)
        #     fact-cache/localhost
        #     cp
        #   playbook_0 (mounted in bwrap for each playbook read-only)
        #     secrets.yaml
        #     project -> ../trusted/project_0/...
        #     role_0 -> ../trusted/project_0/...
        #   trusted (mounted in bwrap read-only)
        #     project_0
        #       <git.example.com>
        #         <project>
        #   untrusted (mounted in bwrap read-only)
        #     project_0
        #       <git.example.com>
        #         <project>
        #   work (mounted in bwrap read-write)
        #     .ssh
        #       known_hosts
        #     .kube
        #       config
        #     src
        #       <git.example.com>
        #         <project>
        #     logs
        #       job-output.txt
        #     tmp
        #     results.json
        self.keep = keep
        if root:
            tmpdir = root
        else:
            tmpdir = tempfile.gettempdir()
        self.root = os.path.realpath(os.path.join(tmpdir, build_uuid))
        os.mkdir(self.root, 0o700)
        self.work_root = os.path.join(self.root, 'work')
        os.makedirs(self.work_root)
        self.src_root = os.path.join(self.work_root, 'src')
        os.makedirs(self.src_root)
        self.log_root = os.path.join(self.work_root, 'logs')
        os.makedirs(self.log_root)
        # Create local tmp directory
        # NOTE(tobiash): This must live within the work root as it can be used
        # by ansible for temporary files which are path checked in untrusted
        # jobs.
        self.local_tmp = os.path.join(self.work_root, 'tmp')
        os.makedirs(self.local_tmp)
        self.ansible_root = os.path.join(self.root, 'ansible')
        os.makedirs(self.ansible_root)
        self.ansible_vars_blacklist = os.path.join(
            self.ansible_root, 'vars_blacklist.yaml')
        with open(self.ansible_vars_blacklist, 'w') as blacklist:
            blacklist.write(json.dumps(BLACKLISTED_VARS))
        self.trusted_root = os.path.join(self.root, 'trusted')
        os.makedirs(self.trusted_root)
        self.untrusted_root = os.path.join(self.root, 'untrusted')
        os.makedirs(self.untrusted_root)
        ssh_dir = os.path.join(self.work_root, '.ssh')
        os.mkdir(ssh_dir, 0o700)
        kube_dir = os.path.join(self.work_root, ".kube")
        os.makedirs(kube_dir)
        self.kubeconfig = os.path.join(kube_dir, "config")
        # Create ansible cache directory
        self.ansible_cache_root = os.path.join(self.root, '.ansible')
        self.fact_cache = os.path.join(self.ansible_cache_root, 'fact-cache')
        os.makedirs(self.fact_cache)
        self.control_path = os.path.join(self.ansible_cache_root, 'cp')
        self.job_unreachable_file = os.path.join(self.ansible_cache_root,
                                                 'nodes.unreachable')
        os.makedirs(self.control_path)

        localhost_facts = os.path.join(self.fact_cache, 'localhost')
        jobtime = datetime.datetime.utcnow()
        date_time_facts = {}
        date_time_facts['year'] = jobtime.strftime('%Y')
        date_time_facts['month'] = jobtime.strftime('%m')
        date_time_facts['weekday'] = jobtime.strftime('%A')
        date_time_facts['weekday_number'] = jobtime.strftime('%w')
        date_time_facts['weeknumber'] = jobtime.strftime('%W')
        date_time_facts['day'] = jobtime.strftime('%d')
        date_time_facts['hour'] = jobtime.strftime('%H')
        date_time_facts['minute'] = jobtime.strftime('%M')
        date_time_facts['second'] = jobtime.strftime('%S')
        date_time_facts['epoch'] = jobtime.strftime('%s')
        date_time_facts['date'] = jobtime.strftime('%Y-%m-%d')
        date_time_facts['time'] = jobtime.strftime('%H:%M:%S')
        date_time_facts['iso8601_micro'] = \
            jobtime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        date_time_facts['iso8601'] = \
            jobtime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        date_time_facts['iso8601_basic'] = jobtime.strftime("%Y%m%dT%H%M%S%f")
        date_time_facts['iso8601_basic_short'] = \
            jobtime.strftime("%Y%m%dT%H%M%S")

        # Set the TZ data manually as jobtime is naive.
        date_time_facts['tz'] = 'UTC'
        date_time_facts['tz_offset'] = '+0000'

        executor_facts = {}
        executor_facts['date_time'] = date_time_facts
        executor_facts['module_setup'] = True

        # NOTE(pabelanger): We do not want to leak zuul-executor facts to other
        # playbooks now that smart fact gathering is enabled by default.  We
        # can have ansible skip populating the cache with information by
        # writing a file with the minimum facts we want.
        with open(localhost_facts, 'w') as f:
            json.dump(executor_facts, f)

        self.result_data_file = os.path.join(self.work_root, 'results.json')
        with open(self.result_data_file, 'w'):
            pass
        self.known_hosts = os.path.join(ssh_dir, 'known_hosts')
        self.inventory = os.path.join(self.ansible_root, 'inventory.yaml')
        self.extra_vars = os.path.join(self.ansible_root, 'extra_vars.yaml')
        self.setup_inventory = os.path.join(self.ansible_root,
                                            'setup-inventory.yaml')
        self.logging_json = os.path.join(self.ansible_root, 'logging.json')
        self.playbooks = []  # The list of candidate playbooks
        self.pre_playbooks = []
        self.post_playbooks = []
        self.cleanup_playbooks = []
        self.job_output_file = os.path.join(self.log_root, 'job-output.txt')
        # We need to create the job-output.txt upfront in order to close the
        # gap between url reporting and ansible creating the file. Otherwise
        # there is a period of time where the user can click on the live log
        # link on the status page but the log streaming fails because the file
        # is not there yet.
        with open(self.job_output_file, 'w') as job_output:
            job_output.write("{now} | Job console starting...\n".format(
                now=datetime.datetime.now()
            ))
        self.trusted_projects = []
        self.trusted_project_index = {}
        self.untrusted_projects = []
        self.untrusted_project_index = {}

        # Create a JobDirPlaybook for the Ansible setup run.  This
        # doesn't use an actual playbook, but it lets us use the same
        # methods to write an ansible.cfg as the rest of the Ansible
        # runs.
        setup_root = os.path.join(self.ansible_root, 'setup_playbook')
        os.makedirs(setup_root)
        self.setup_playbook = JobDirPlaybook(setup_root)
        self.setup_playbook.trusted = True

    def addTrustedProject(self, canonical_name, branch):
        # Trusted projects are placed in their own directories so that
        # we can support using different branches of the same project
        # in different playbooks.
        count = len(self.trusted_projects)
        root = os.path.join(self.trusted_root, 'project_%i' % (count,))
        os.makedirs(root)
        self.trusted_projects.append(root)
        self.trusted_project_index[(canonical_name, branch)] = root
        return root

    def getTrustedProject(self, canonical_name, branch):
        return self.trusted_project_index.get((canonical_name, branch))

    def addUntrustedProject(self, canonical_name, branch):
        # Similar to trusted projects, but these hold checkouts of
        # projects which are allowed to have speculative changes
        # applied.  They might, however, be different branches than
        # what is used in the working dir, so they need their own
        # location.  Moreover, we might avoid mischief if a job alters
        # the contents of the working dir.
        count = len(self.untrusted_projects)
        root = os.path.join(self.untrusted_root, 'project_%i' % (count,))
        os.makedirs(root)
        self.untrusted_projects.append(root)
        self.untrusted_project_index[(canonical_name, branch)] = root
        return root

    def getUntrustedProject(self, canonical_name, branch):
        return self.untrusted_project_index.get((canonical_name, branch))

    def addPrePlaybook(self):
        count = len(self.pre_playbooks)
        root = os.path.join(self.ansible_root, 'pre_playbook_%i' % (count,))
        os.makedirs(root)
        playbook = JobDirPlaybook(root)
        self.pre_playbooks.append(playbook)
        return playbook

    def addPostPlaybook(self):
        count = len(self.post_playbooks)
        root = os.path.join(self.ansible_root, 'post_playbook_%i' % (count,))
        os.makedirs(root)
        playbook = JobDirPlaybook(root)
        self.post_playbooks.append(playbook)
        return playbook

    def addCleanupPlaybook(self):
        count = len(self.cleanup_playbooks)
        root = os.path.join(
            self.ansible_root, 'cleanup_playbook_%i' % (count,))
        os.makedirs(root)
        playbook = JobDirPlaybook(root)
        self.cleanup_playbooks.append(playbook)
        return playbook

    def addPlaybook(self):
        count = len(self.playbooks)
        root = os.path.join(self.ansible_root, 'playbook_%i' % (count,))
        os.makedirs(root)
        playbook = JobDirPlaybook(root)
        self.playbooks.append(playbook)
        return playbook

    def cleanup(self):
        if not self.keep:
            shutil.rmtree(self.root)

    def __enter__(self):
        return self

    def __exit__(self, etype, value, tb):
        self.cleanup()


class UpdateTask(object):
    def __init__(self, connection_name, project_name, repo_state=None,
                 zuul_event_id=None, build=None):
        self.connection_name = connection_name
        self.project_name = project_name
        self.repo_state = repo_state
        self.canonical_name = None
        self.branches = None
        self.refs = None
        self.event = threading.Event()
        self.success = False

        # These variables are used for log annotation
        self.zuul_event_id = zuul_event_id
        self.build = build

    def __eq__(self, other):
        if (other and other.connection_name == self.connection_name and
            other.project_name == self.project_name and
            other.repo_state == self.repo_state):
            return True
        return False

    def wait(self):
        self.event.wait()

    def setComplete(self):
        self.event.set()


class DeduplicateQueue(object):
    def __init__(self):
        self.queue = collections.deque()
        self.condition = threading.Condition()

    def qsize(self):
        return len(self.queue)

    def put(self, item):
        # Returns the original item if added, or an equivalent item if
        # already enqueued.
        self.condition.acquire()
        ret = None
        try:
            for x in self.queue:
                if item == x:
                    ret = x
            if ret is None:
                ret = item
                self.queue.append(item)
                self.condition.notify()
        finally:
            self.condition.release()
        return ret

    def get(self):
        self.condition.acquire()
        try:
            while True:
                try:
                    ret = self.queue.popleft()
                    return ret
                except IndexError:
                    pass
                self.condition.wait()
        finally:
            self.condition.release()


def check_varnames(var):
    # We block these in configloader, but block it here too to make
    # sure that a job doesn't pass variables named zuul or nodepool.
    if 'zuul' in var:
        raise Exception("Defining variables named 'zuul' is not allowed")
    if 'nodepool' in var:
        raise Exception("Defining variables named 'nodepool' is not allowed")


def make_setup_inventory_dict(nodes):
    hosts = {}
    for node in nodes:
        if (node['host_vars']['ansible_connection'] in
            BLACKLISTED_ANSIBLE_CONNECTION_TYPES):
            continue
        hosts[node['name']] = node['host_vars']

    inventory = {
        'all': {
            'hosts': hosts,
        }
    }

    return inventory


def is_group_var_set(name, host, args):
    for group in args['groups']:
        if host in group['nodes']:
            group_vars = args['group_vars'].get(group['name'], {})
            if name in group_vars:
                return True
    return False


def make_inventory_dict(nodes, args, all_vars):
    hosts = {}
    for node in nodes:
        hosts[node['name']] = node['host_vars']

    zuul_vars = all_vars['zuul']
    if 'message' in zuul_vars:
        zuul_vars['message'] = base64.b64encode(
            zuul_vars['message'].encode("utf-8")).decode('utf-8')

    inventory = {
        'all': {
            'hosts': hosts,
            'vars': all_vars,
        }
    }

    for group in args['groups']:
        if 'children' not in inventory['all']:
            inventory['all']['children'] = dict()
        group_hosts = {}
        for node_name in group['nodes']:
            group_hosts[node_name] = None
        group_vars = args['group_vars'].get(group['name'], {}).copy()
        check_varnames(group_vars)

        inventory['all']['children'].update({
            group['name']: {
                'hosts': group_hosts,
                'vars': group_vars,
            }})

    return inventory


class AnsibleJob(object):
    RESULT_NORMAL = 1
    RESULT_TIMED_OUT = 2
    RESULT_UNREACHABLE = 3
    RESULT_ABORTED = 4
    RESULT_DISK_FULL = 5

    RESULT_MAP = {
        RESULT_NORMAL: 'RESULT_NORMAL',
        RESULT_TIMED_OUT: 'RESULT_TIMED_OUT',
        RESULT_UNREACHABLE: 'RESULT_UNREACHABLE',
        RESULT_ABORTED: 'RESULT_ABORTED',
        RESULT_DISK_FULL: 'RESULT_DISK_FULL',
    }

    def __init__(self, executor_server, job):
        logger = logging.getLogger("zuul.AnsibleJob")
        self.arguments = json.loads(job.arguments)
        self.zuul_event_id = self.arguments.get('zuul_event_id')
        # Record ansible version being used for the cleanup phase
        self.ansible_version = self.arguments.get('ansible_version')
        self.log = get_annotated_logger(
            logger, self.zuul_event_id, build=job.unique)
        self.executor_server = executor_server
        self.job = job
        self.jobdir = None
        self.proc = None
        self.proc_lock = threading.Lock()
        self.running = False
        self.started = False  # Whether playbooks have started running
        self.time_starting_build = None
        self.paused = False
        self.aborted = False
        self.aborted_reason = None
        self.cleanup_started = False
        self._resume_event = threading.Event()
        self.thread = None
        self.project_info = {}
        self.private_key_file = get_default(self.executor_server.config,
                                            'executor', 'private_key_file',
                                            '~/.ssh/id_rsa')
        self.winrm_key_file = get_default(self.executor_server.config,
                                          'executor', 'winrm_cert_key_file',
                                          '~/.winrm/winrm_client_cert.key')
        self.winrm_pem_file = get_default(self.executor_server.config,
                                          'executor', 'winrm_cert_pem_file',
                                          '~/.winrm/winrm_client_cert.pem')
        self.winrm_operation_timeout = get_default(
            self.executor_server.config,
            'executor',
            'winrm_operation_timeout_sec')
        self.winrm_read_timeout = get_default(
            self.executor_server.config,
            'executor',
            'winrm_read_timeout_sec')
        self.ssh_agent = SshAgent(zuul_event_id=self.zuul_event_id,
                                  build=self.job.unique)
        self.port_forwards = []
        self.executor_variables_file = None

        self.cpu_times = {'user': 0, 'system': 0,
                          'children_user': 0, 'children_system': 0}

        if self.executor_server.config.has_option('executor', 'variables'):
            self.executor_variables_file = self.executor_server.config.get(
                'executor', 'variables')

        plugin_dir = self.executor_server.ansible_manager.getAnsiblePluginDir(
            self.arguments.get('ansible_version'))
        self.ara_callbacks = \
            self.executor_server.ansible_manager.getAraCallbackPlugin(
                self.arguments.get('ansible_version'))
        self.library_dir = os.path.join(plugin_dir, 'library')
        self.action_dir = os.path.join(plugin_dir, 'action')
        self.action_dir_general = os.path.join(plugin_dir, 'actiongeneral')
        self.action_dir_trusted = os.path.join(plugin_dir, 'actiontrusted')
        self.callback_dir = os.path.join(plugin_dir, 'callback')
        self.lookup_dir = os.path.join(plugin_dir, 'lookup')
        self.filter_dir = os.path.join(plugin_dir, 'filter')
        self.ansible_callbacks = self.executor_server.ansible_callbacks

    def run(self):
        self.running = True
        self.thread = threading.Thread(target=self.execute,
                                       name='build-%s' % self.job.unique)
        self.thread.start()

    def stop(self, reason=None):
        self.aborted = True
        self.aborted_reason = reason

        # if paused we need to resume the job so it can be stopped
        self.resume()
        self.abortRunningProc()

    def pause(self):
        self.log.info(
            "Pausing job %s for ref %s (change %s)" % (
                self.arguments['zuul']['job'],
                self.arguments['zuul']['ref'],
                self.arguments['zuul']['change_url']))
        with open(self.jobdir.job_output_file, 'a') as job_output:
            job_output.write(
                "{now} |\n"
                "{now} | Job paused\n".format(now=datetime.datetime.now()))

        self.paused = True

        data = {'paused': self.paused, 'data': self.getResultData()}
        self.job.sendWorkData(json.dumps(data))
        self._resume_event.wait()

    def resume(self):
        if not self.paused:
            return

        self.log.info(
            "Resuming job %s for ref %s (change %s)" % (
                self.arguments['zuul']['job'],
                self.arguments['zuul']['ref'],
                self.arguments['zuul']['change_url']))
        with open(self.jobdir.job_output_file, 'a') as job_output:
            job_output.write(
                "{now} | Job resumed\n"
                "{now} |\n".format(now=datetime.datetime.now()))

        self.paused = False
        self._resume_event.set()

    def wait(self):
        if self.thread:
            self.thread.join()

    def execute(self):
        try:
            self.time_starting_build = time.monotonic()

            # report that job has been taken
            self.job.sendWorkData(json.dumps(self._base_job_data()))

            self.ssh_agent.start()
            self.ssh_agent.add(self.private_key_file)
            for key in self.arguments.get('ssh_keys', []):
                self.ssh_agent.addData(key['name'], key['key'])
            self.jobdir = JobDir(self.executor_server.jobdir_root,
                                 self.executor_server.keep_jobdir,
                                 str(self.job.unique))
            self._execute()
        except BrokenProcessPool:
            # The process pool got broken, re-initialize it and send
            # ABORTED so we re-try the job.
            self.log.exception('Process pool got broken')
            self.executor_server.resetProcessPool()
            self._send_aborted()
        except ExecutorError as e:
            result_data = json.dumps(dict(result='ERROR',
                                          error_detail=e.args[0]))
            self.log.debug("Sending result: %s" % (result_data,))
            self.job.sendWorkComplete(result_data)
        except Exception:
            self.log.exception("Exception while executing job")
            self.job.sendWorkException(traceback.format_exc())
        finally:
            self.running = False
            if self.jobdir:
                try:
                    self.jobdir.cleanup()
                except Exception:
                    self.log.exception("Error cleaning up jobdir:")
            if self.ssh_agent:
                try:
                    self.ssh_agent.stop()
                except Exception:
                    self.log.exception("Error stopping SSH agent:")
            for fwd in self.port_forwards:
                try:
                    fwd.stop()
                except Exception:
                    self.log.exception("Error stopping port forward:")
            try:
                self.executor_server.finishJob(self.job.unique)
            except Exception:
                self.log.exception("Error finalizing job thread:")
            self.log.info("Job execution took: %.3f seconds" % (
                time.monotonic() - self.time_starting_build))

    def _base_job_data(self):
        return {
            # TODO(mordred) worker_name is needed as a unique name for the
            # client to use for cancelling jobs on an executor. It's
            # defaulting to the hostname for now, but in the future we
            # should allow setting a per-executor override so that one can
            # run more than one executor on a host.
            'worker_name': self.executor_server.hostname,
            'worker_hostname': self.executor_server.hostname,
            'worker_log_port': self.executor_server.log_streaming_port,
        }

    def _send_aborted(self):
        result = dict(result='ABORTED')
        self.job.sendWorkComplete(json.dumps(result))

    def _execute(self):
        args = self.arguments
        self.log.info(
            "Beginning job %s for ref %s (change %s)" % (
                args['zuul']['job'],
                args['zuul']['ref'],
                args['zuul']['change_url']))
        self.log.debug("Job root: %s" % (self.jobdir.root,))
        tasks = []
        projects = set()
        repo_state = args['repo_state']

        # Make sure all projects used by the job are updated...
        for project in args['projects']:
            self.log.debug("Updating project %s" % (project,))
            tasks.append(self.executor_server.update(
                project['connection'], project['name'],
                repo_state=repo_state,
                zuul_event_id=self.zuul_event_id,
                build=self.job.unique))
            projects.add((project['connection'], project['name']))

        # ...as well as all playbook and role projects.
        repos = []
        playbooks = (args['pre_playbooks'] + args['playbooks'] +
                     args['post_playbooks'] + args['cleanup_playbooks'])
        for playbook in playbooks:
            repos.append(playbook)
            repos += playbook['roles']

        for repo in repos:
            key = (repo['connection'], repo['project'])
            if key not in projects:
                self.log.debug("Updating playbook or role %s" % (
                               repo['project'],))
                tasks.append(self.executor_server.update(
                    *key, repo_state=repo_state,
                    zuul_event_id=self.zuul_event_id,
                    build=self.job.unique))
                projects.add(key)

        for task in tasks:
            task.wait()

            if not task.success:
                raise ExecutorError(
                    'Failed to update project %s' % task.canonical_name)

            self.project_info[task.canonical_name] = {
                'refs': task.refs,
                'branches': task.branches,
            }

        # Early abort if abort requested
        if self.aborted:
            self._send_aborted()
            return

        self.log.debug("Git updates complete")
        merger = self.executor_server._getMerger(
            self.jobdir.src_root,
            self.executor_server.merge_root,
            self.log)
        repos = {}
        for project in args['projects']:
            self.log.debug("Cloning %s/%s" % (project['connection'],
                                              project['name'],))
            repo = merger.getRepo(project['connection'],
                                  project['name'])
            repos[project['canonical_name']] = repo

        # The commit ID of the original item (before merging).  Used
        # later for line mapping.
        item_commit = None

        merge_items = [i for i in args['items'] if i.get('number')]
        if merge_items:
            item_commit = self.doMergeChanges(
                merger, merge_items, repo_state)
            if item_commit is None:
                # There was a merge conflict and we have already sent
                # a work complete result, don't run any jobs
                return

        # Early abort if abort requested
        if self.aborted:
            self._send_aborted()
            return

        state_items = [i for i in args['items'] if not i.get('number')]
        if state_items:
            merger.setRepoState(
                state_items, repo_state,
                process_worker=self.executor_server.process_worker)

        # Early abort if abort requested
        if self.aborted:
            self._send_aborted()
            return

        for project in args['projects']:
            repo = repos[project['canonical_name']]
            # If this project is the Zuul project and this is a ref
            # rather than a change, checkout the ref.
            if (project['canonical_name'] ==
                args['zuul']['project']['canonical_name'] and
                (not args['zuul'].get('branch')) and
                args['zuul'].get('ref')):
                ref = args['zuul']['ref']
            else:
                ref = None
            selected_ref, selected_desc = self.resolveBranch(
                project['canonical_name'],
                ref,
                args['branch'],
                args['override_branch'],
                args['override_checkout'],
                project['override_branch'],
                project['override_checkout'],
                project['default_branch'])
            self.log.info("Checking out %s %s %s",
                          project['canonical_name'], selected_desc,
                          selected_ref)
            repo.checkout(selected_ref)

            # Update the inventory variables to indicate the ref we
            # checked out
            p = args['zuul']['projects'][project['canonical_name']]
            p['checkout'] = selected_ref

        # Set the URL of the origin remote for each repo to a bogus
        # value. Keeping the remote allows tools to use it to determine
        # which commits are part of the current change.
        for repo in repos.values():
            repo.setRemoteUrl('file:///dev/null')

        # Early abort if abort requested
        if self.aborted:
            self._send_aborted()
            return

        # This prepares each playbook and the roles needed for each.
        self.preparePlaybooks(args)

        self.prepareAnsibleFiles(args)
        self.writeLoggingConfig()

        # Early abort if abort requested
        if self.aborted:
            self._send_aborted()
            return

        data = self._base_job_data()
        if self.executor_server.log_streaming_port != DEFAULT_FINGER_PORT:
            data['url'] = "finger://{hostname}:{port}/{uuid}".format(
                hostname=self.executor_server.hostname,
                port=self.executor_server.log_streaming_port,
                uuid=self.job.unique)
        else:
            data['url'] = 'finger://{hostname}/{uuid}'.format(
                hostname=self.executor_server.hostname,
                uuid=self.job.unique)

        self.job.sendWorkData(json.dumps(data))
        self.job.sendWorkStatus(0, 100)

        result = self.runPlaybooks(args)
        success = result == 'SUCCESS'

        self.runCleanupPlaybooks(success)

        # Stop the persistent SSH connections.
        setup_status, setup_code = self.runAnsibleCleanup(
            self.jobdir.setup_playbook)

        if self.aborted_reason == self.RESULT_DISK_FULL:
            result = 'DISK_FULL'
        data = self.getResultData()
        warnings = []
        self.mapLines(merger, args, data, item_commit, warnings)
        warnings.extend(get_warnings_from_result_data(data, logger=self.log))
        result_data = json.dumps(dict(result=result,
                                      warnings=warnings,
                                      data=data))
        self.log.debug("Sending result: %s" % (result_data,))
        self.job.sendWorkComplete(result_data)

    def getResultData(self):
        data = {}
        try:
            with open(self.jobdir.result_data_file) as f:
                file_data = f.read()
                if file_data:
                    data = json.loads(file_data)
        except Exception:
            self.log.exception("Unable to load result data:")
        return data

    def mapLines(self, merger, args, data, commit, warnings):
        # The data and warnings arguments are mutated in this method.

        # If we received file comments, map the line numbers before
        # we send the result.
        fc = data.get('zuul', {}).get('file_comments')
        if not fc:
            return
        disable = data.get('zuul', {}).get('disable_file_comment_line_mapping')
        if disable:
            return

        try:
            filecomments.validate(fc)
        except Exception as e:
            warnings.append("Job %s: validation error in file comments: %s" %
                            (args['zuul']['job'], str(e)))
            del data['zuul']['file_comments']
            return

        repo = None
        for project in args['projects']:
            if (project['canonical_name'] !=
                args['zuul']['project']['canonical_name']):
                continue
            repo = merger.getRepo(project['connection'],
                                  project['name'])
        # If the repo doesn't exist, abort
        if not repo:
            return

        # Check out the selected ref again in case the job altered the
        # repo state.
        p = args['zuul']['projects'][project['canonical_name']]
        selected_ref = p['checkout']

        self.log.info("Checking out %s %s for line mapping",
                      project['canonical_name'], selected_ref)
        try:
            repo.checkout(selected_ref)
        except Exception:
            # If checkout fails, abort
            self.log.exception("Error checking out repo for line mapping")
            warnings.append("Job %s: unable to check out repo "
                            "for file comments" % (args['zuul']['job']))
            return

        lines = filecomments.extractLines(fc)

        new_lines = {}
        for (filename, lineno) in lines:
            try:
                new_lineno = repo.mapLine(commit, filename, lineno)
            except Exception as e:
                # Log at debug level since it's likely a job issue
                self.log.debug("Error mapping line:", exc_info=True)
                if isinstance(e, git.GitCommandError):
                    msg = e.stderr
                else:
                    msg = str(e)
                warnings.append("Job %s: unable to map line "
                                "for file comments: %s" %
                                (args['zuul']['job'], msg))
                new_lineno = None
            if new_lineno is not None:
                new_lines[(filename, lineno)] = new_lineno

        filecomments.updateLines(fc, new_lines)

    def doMergeChanges(self, merger, items, repo_state):
        try:
            ret = merger.mergeChanges(
                items, repo_state=repo_state,
                process_worker=self.executor_server.process_worker)
        except ValueError:
            # Return ABORTED so that we'll try again. At this point all of
            # the refs we're trying to merge should be valid refs. If we
            # can't fetch them, it should resolve itself.
            self.log.exception("Could not fetch refs to merge from remote")
            result = dict(result='ABORTED')
            self.job.sendWorkComplete(json.dumps(result))
            return None
        if not ret:  # merge conflict
            result = dict(result='MERGER_FAILURE')
            if self.executor_server.statsd:
                base_key = "zuul.executor.{hostname}.merger"
                self.executor_server.statsd.incr(base_key + ".FAILURE")
            self.job.sendWorkComplete(json.dumps(result))
            return None

        if self.executor_server.statsd:
            base_key = "zuul.executor.{hostname}.merger"
            self.executor_server.statsd.incr(base_key + ".SUCCESS")
        recent = ret[3]
        orig_commit = ret[4]
        for key, commit in recent.items():
            (connection, project, branch) = key
            # Compare the commit with the repo state. If it's included in the
            # repo state and it's the same we've set this ref already earlier
            # and don't have to set it again.
            repo_state_project = repo_state.get(
                connection, {}).get(project, {})
            repo_state_commit = repo_state_project.get(
                'refs/heads/%s' % branch)
            if repo_state_commit != commit:
                repo = merger.getRepo(connection, project)
                repo.setRef('refs/heads/' + branch, commit)
        return orig_commit

    def resolveBranch(self, project_canonical_name, ref, zuul_branch,
                      job_override_branch, job_override_checkout,
                      project_override_branch, project_override_checkout,
                      project_default_branch):
        branches = self.project_info[project_canonical_name]['branches']
        refs = self.project_info[project_canonical_name]['refs']
        selected_ref = None
        selected_desc = None
        if project_override_checkout in refs:
            selected_ref = project_override_checkout
            selected_desc = 'project override ref'
        elif project_override_branch in branches:
            selected_ref = project_override_branch
            selected_desc = 'project override branch'
        elif job_override_checkout in refs:
            selected_ref = job_override_checkout
            selected_desc = 'job override ref'
        elif job_override_branch in branches:
            selected_ref = job_override_branch
            selected_desc = 'job override branch'
        elif ref and ref.startswith('refs/heads/'):
            selected_ref = ref[len('refs/heads/'):]
            selected_desc = 'branch ref'
        elif ref and ref.startswith('refs/tags/'):
            selected_ref = ref[len('refs/tags/'):]
            selected_desc = 'tag ref'
        elif zuul_branch and zuul_branch in branches:
            selected_ref = zuul_branch
            selected_desc = 'zuul branch'
        elif project_default_branch in branches:
            selected_ref = project_default_branch
            selected_desc = 'project default branch'
        else:
            raise ExecutorError("Project %s does not have the "
                                "default branch %s" %
                                (project_canonical_name,
                                 project_default_branch))
        return (selected_ref, selected_desc)

    def getAnsibleTimeout(self, start, timeout):
        if timeout is not None:
            now = time.time()
            elapsed = now - start
            timeout = timeout - elapsed
        return timeout

    def runPlaybooks(self, args):
        result = None

        with open(self.jobdir.job_output_file, 'a') as job_output:
            job_output.write("{now} | Running Ansible setup...\n".format(
                now=datetime.datetime.now()
            ))
        # Run the Ansible 'setup' module on all hosts in the inventory
        # at the start of the job with a 60 second timeout.  If we
        # aren't able to connect to all the hosts and gather facts
        # within that timeout, there is likely a network problem
        # between here and the hosts in the inventory; return them and
        # reschedule the job.
        setup_status, setup_code = self.runAnsibleSetup(
            self.jobdir.setup_playbook, self.ansible_version)
        if setup_status != self.RESULT_NORMAL or setup_code != 0:
            return result

        pre_failed = False
        success = False
        if self.executor_server.statsd:
            key = "zuul.executor.{hostname}.starting_builds"
            self.executor_server.statsd.timing(
                key, (time.monotonic() - self.time_starting_build) * 1000)

        self.started = True
        time_started = time.time()
        # timeout value is "total" job timeout which accounts for
        # pre-run and run playbooks. post-run is different because
        # it is used to copy out job logs and we want to do our best
        # to copy logs even when the job has timed out.
        job_timeout = args['timeout']
        for index, playbook in enumerate(self.jobdir.pre_playbooks):
            # TODOv3(pabelanger): Implement pre-run timeout setting.
            ansible_timeout = self.getAnsibleTimeout(time_started, job_timeout)
            pre_status, pre_code = self.runAnsiblePlaybook(
                playbook, ansible_timeout, self.ansible_version, phase='pre',
                index=index)
            if pre_status != self.RESULT_NORMAL or pre_code != 0:
                # These should really never fail, so return None and have
                # zuul try again
                pre_failed = True
                break

        self.log.debug(
            "Overall ansible cpu times: user=%.2f, system=%.2f, "
            "children_user=%.2f, children_system=%.2f" %
            (self.cpu_times['user'], self.cpu_times['system'],
             self.cpu_times['children_user'],
             self.cpu_times['children_system']))

        if not pre_failed:
            for index, playbook in enumerate(self.jobdir.playbooks):
                ansible_timeout = self.getAnsibleTimeout(
                    time_started, job_timeout)
                job_status, job_code = self.runAnsiblePlaybook(
                    playbook, ansible_timeout, self.ansible_version,
                    phase='run', index=index)
                if job_status == self.RESULT_ABORTED:
                    return 'ABORTED'
                elif job_status == self.RESULT_TIMED_OUT:
                    # Set the pre-failure flag so this doesn't get
                    # overridden by a post-failure.
                    pre_failed = True
                    result = 'TIMED_OUT'
                    break
                elif job_status == self.RESULT_NORMAL:
                    success = (job_code == 0)
                    if success:
                        result = 'SUCCESS'
                    else:
                        result = 'FAILURE'
                        break
                else:
                    # The result of the job is indeterminate.  Zuul will
                    # run it again.
                    return None

        # check if we need to pause here
        result_data = self.getResultData()
        pause = result_data.get('zuul', {}).get('pause')
        if success and pause:
            self.pause()
        if self.aborted:
            return 'ABORTED'

        post_timeout = args['post_timeout']
        unreachable = False
        for index, playbook in enumerate(self.jobdir.post_playbooks):
            # Post timeout operates a little differently to the main job
            # timeout. We give each post playbook the full post timeout to
            # do its job because post is where you'll often record job logs
            # which are vital to understanding why timeouts have happened in
            # the first place.
            post_status, post_code = self.runAnsiblePlaybook(
                playbook, post_timeout, self.ansible_version, success,
                phase='post', index=index)
            if post_status == self.RESULT_ABORTED:
                return 'ABORTED'
            if post_status == self.RESULT_UNREACHABLE:
                # In case we encounter unreachable nodes we need to return None
                # so the job can be retried. However in the case of post
                # playbooks we should still try to run all playbooks to get a
                # chance to upload logs.
                unreachable = True
            if post_status != self.RESULT_NORMAL or post_code != 0:
                success = False
                # If we encountered a pre-failure, that takes
                # precedence over the post result.
                if not pre_failed:
                    result = 'POST_FAILURE'
                if (index + 1) == len(self.jobdir.post_playbooks):
                    self._logFinalPlaybookError()

        if unreachable:
            return None

        return result

    def runCleanupPlaybooks(self, success):
        if not self.jobdir.cleanup_playbooks:
            return

        # TODO: make this configurable
        cleanup_timeout = 300

        with open(self.jobdir.job_output_file, 'a') as job_output:
            job_output.write("{now} | Running Ansible cleanup...\n".format(
                now=datetime.datetime.now()
            ))

        self.cleanup_started = True
        for index, playbook in enumerate(self.jobdir.cleanup_playbooks):
            self.runAnsiblePlaybook(
                playbook, cleanup_timeout, self.ansible_version,
                success=success, phase='cleanup', index=index)

    def _logFinalPlaybookError(self):
        # Failures in the final post playbook can include failures
        # uploading logs, which makes diagnosing issues difficult.
        # Grab the output from the last playbook from the json
        # file and log it.
        json_output = self.jobdir.job_output_file.replace('txt', 'json')
        self.log.debug("Final playbook failed")
        if not os.path.exists(json_output):
            self.log.debug("JSON logfile {logfile} is missing".format(
                logfile=json_output))
            return
        try:
            output = json.load(open(json_output, 'r'))
            last_playbook = output[-1]
            # Transform json to yaml - because it's easier to read and given
            # the size of the data it'll be extra-hard to read this as an
            # all on one line stringified nested dict.
            yaml_out = yaml.safe_dump(last_playbook, default_flow_style=False)
            for line in yaml_out.split('\n'):
                self.log.debug(line)
        except Exception:
            self.log.exception(
                "Could not decode json from {logfile}".format(
                    logfile=json_output))

    def getHostList(self, args):
        hosts = []
        for node in args['nodes']:
            # NOTE(mordred): This assumes that the nodepool launcher
            # and the zuul executor both have similar network
            # characteristics, as the launcher will do a test for ipv6
            # viability and if so, and if the node has an ipv6
            # address, it will be the interface_ip.  force-ipv4 can be
            # set to True in the clouds.yaml for a cloud if this
            # results in the wrong thing being in interface_ip
            # TODO(jeblair): Move this notice to the docs.
            for name in node['name']:
                ip = node.get('interface_ip')
                port = node.get('connection_port', node.get('ssh_port', 22))
                host_vars = args['host_vars'].get(name, {}).copy()
                check_varnames(host_vars)
                host_vars.update(dict(
                    ansible_host=ip,
                    ansible_user=self.executor_server.default_username,
                    ansible_port=port,
                    nodepool=dict(
                        label=node.get('label'),
                        az=node.get('az'),
                        cloud=node.get('cloud'),
                        provider=node.get('provider'),
                        region=node.get('region'),
                        host_id=node.get('host_id'),
                        interface_ip=node.get('interface_ip'),
                        public_ipv4=node.get('public_ipv4'),
                        private_ipv4=node.get('private_ipv4'),
                        public_ipv6=node.get('public_ipv6'))))

                # Ansible >=2.8 introduced "auto" as an
                # ansible_python_interpreter argument that looks up
                # which python to use on the remote host in an inbuilt
                # table and essentially "does the right thing"
                # (i.e. chooses python3 on 3-only hosts like later
                # Fedoras).
                # If ansible_python_interpreter is set either as a group
                # var or all-var, then don't do anything here; let the
                # user control.
                api = 'ansible_python_interpreter'
                if (api not in args['vars'] and
                    not is_group_var_set(api, name, args)):
                    python = node.get('python_path', 'auto')
                    host_vars.setdefault(api, python)

                username = node.get('username')
                if username:
                    host_vars['ansible_user'] = username

                connection_type = node.get('connection_type')
                if connection_type:
                    host_vars['ansible_connection'] = connection_type
                    if connection_type == "winrm":
                        host_vars['ansible_winrm_transport'] = 'certificate'
                        host_vars['ansible_winrm_cert_pem'] = \
                            self.winrm_pem_file
                        host_vars['ansible_winrm_cert_key_pem'] = \
                            self.winrm_key_file
                        # NOTE(tobiash): This is necessary when using default
                        # winrm self-signed certificates. This is probably what
                        # most installations want so hard code this here for
                        # now.
                        host_vars['ansible_winrm_server_cert_validation'] = \
                            'ignore'
                        if self.winrm_operation_timeout is not None:
                            host_vars['ansible_winrm_operation_timeout_sec'] =\
                                self.winrm_operation_timeout
                        if self.winrm_read_timeout is not None:
                            host_vars['ansible_winrm_read_timeout_sec'] = \
                                self.winrm_read_timeout
                    elif connection_type == "kubectl":
                        host_vars['ansible_kubectl_context'] = \
                            node.get('kubectl_context')

                shell_type = node.get('shell_type')
                if shell_type:
                    host_vars['ansible_shell_type'] = shell_type

                host_keys = []
                for key in node.get('host_keys', []):
                    if port != 22:
                        host_keys.append("[%s]:%s %s" % (ip, port, key))
                    else:
                        host_keys.append("%s %s" % (ip, key))
                if not node.get('host_keys'):
                    host_vars['ansible_ssh_common_args'] = \
                        '-o StrictHostKeyChecking=false'

                hosts.append(dict(
                    name=name,
                    host_vars=host_vars,
                    host_keys=host_keys))
        return hosts

    def _blockPluginDirs(self, path):
        '''Prevent execution of playbooks or roles with plugins

        Plugins are loaded from roles and also if there is a plugin
        dir adjacent to the playbook.  Throw an error if the path
        contains a location that would cause a plugin to get loaded.

        '''
        for entry in os.listdir(path):
            entry = os.path.join(path, entry)
            if os.path.isdir(entry) and entry.endswith('_plugins'):
                raise PluginFoundError(
                    "Ansible plugin dir %s found adjacent to playbook %s in "
                    "non-trusted repo." % (entry, path))

    def findPlaybook(self, path, trusted=False):
        if os.path.exists(path):
            if not trusted:
                # Plugins can be defined in multiple locations within the
                # playbook's subtree.
                #
                #  1. directly within the playbook:
                #       block playbook_dir/*_plugins
                #
                #  2. within a role defined in playbook_dir/<rolename>:
                #       block playbook_dir/*/*_plugins
                #
                #  3. within a role defined in playbook_dir/roles/<rolename>:
                #       block playbook_dir/roles/*/*_plugins

                playbook_dir = os.path.dirname(os.path.abspath(path))
                paths_to_check = []

                def addPathsToCheck(root_dir):
                    if os.path.isdir(root_dir):
                        for entry in os.listdir(root_dir):
                            entry = os.path.join(root_dir, entry)
                            if os.path.isdir(entry):
                                paths_to_check.append(entry)

                # handle case 1
                paths_to_check.append(playbook_dir)

                # handle case 2
                addPathsToCheck(playbook_dir)

                # handle case 3
                addPathsToCheck(os.path.join(playbook_dir, 'roles'))

                for path_to_check in paths_to_check:
                    self._blockPluginDirs(path_to_check)

            return path
        raise ExecutorError("Unable to find playbook %s" % path)

    def preparePlaybooks(self, args):
        self.writeAnsibleConfig(self.jobdir.setup_playbook)

        for playbook in args['pre_playbooks']:
            jobdir_playbook = self.jobdir.addPrePlaybook()
            self.preparePlaybook(jobdir_playbook, playbook, args)

        job_playbook = None
        for playbook in args['playbooks']:
            jobdir_playbook = self.jobdir.addPlaybook()
            self.preparePlaybook(jobdir_playbook, playbook, args)
            if jobdir_playbook.path is not None:
                if job_playbook is None:
                    job_playbook = jobdir_playbook

        if job_playbook is None:
            raise ExecutorError("No playbook specified")

        for playbook in args['post_playbooks']:
            jobdir_playbook = self.jobdir.addPostPlaybook()
            self.preparePlaybook(jobdir_playbook, playbook, args)

        for playbook in args['cleanup_playbooks']:
            jobdir_playbook = self.jobdir.addCleanupPlaybook()
            self.preparePlaybook(jobdir_playbook, playbook, args)

    def preparePlaybook(self, jobdir_playbook, playbook, args):
        # Check out the playbook repo if needed and set the path to
        # the playbook that should be run.
        self.log.debug("Prepare playbook repo for %s: %s@%s" %
                       (playbook['trusted'] and 'trusted' or 'untrusted',
                        playbook['project'], playbook['branch']))
        source = self.executor_server.connections.getSource(
            playbook['connection'])
        project = source.getProject(playbook['project'])
        branch = playbook['branch']
        jobdir_playbook.trusted = playbook['trusted']
        jobdir_playbook.branch = branch
        jobdir_playbook.project_canonical_name = project.canonical_name
        jobdir_playbook.canonical_name_and_path = os.path.join(
            project.canonical_name, playbook['path'])
        path = None

        if not jobdir_playbook.trusted:
            path = self.checkoutUntrustedProject(project, branch, args)
        else:
            path = self.checkoutTrustedProject(project, branch)
        path = os.path.join(path, playbook['path'])

        jobdir_playbook.path = self.findPlaybook(
            path,
            trusted=jobdir_playbook.trusted)

        # If this playbook doesn't exist, don't bother preparing
        # roles.
        if not jobdir_playbook.path:
            return

        for role in playbook['roles']:
            self.prepareRole(jobdir_playbook, role, args)

        secrets = playbook['secrets']
        if secrets:
            check_varnames(secrets)
            jobdir_playbook.secrets_content = yaml.safe_dump(
                secrets, default_flow_style=False)

        self.writeAnsibleConfig(jobdir_playbook)

    def checkoutTrustedProject(self, project, branch):
        root = self.jobdir.getTrustedProject(project.canonical_name,
                                             branch)
        if not root:
            root = self.jobdir.addTrustedProject(project.canonical_name,
                                                 branch)
            self.log.debug("Cloning %s@%s into new trusted space %s",
                           project, branch, root)
            merger = self.executor_server._getMerger(
                root,
                self.executor_server.merge_root,
                self.log)
            merger.checkoutBranch(project.connection_name, project.name,
                                  branch)
        else:
            self.log.debug("Using existing repo %s@%s in trusted space %s",
                           project, branch, root)

        path = os.path.join(root,
                            project.canonical_hostname,
                            project.name)
        return path

    def checkoutUntrustedProject(self, project, branch, args):
        root = self.jobdir.getUntrustedProject(project.canonical_name,
                                               branch)
        if not root:
            root = self.jobdir.addUntrustedProject(project.canonical_name,
                                                   branch)
            # If the project is in the dependency chain, clone from
            # there so we pick up any speculative changes, otherwise,
            # clone from the cache.
            merger = None
            for p in args['projects']:
                if (p['connection'] == project.connection_name and
                    p['name'] == project.name):
                    # We already have this repo prepared
                    self.log.debug("Found workdir repo for untrusted project")
                    merger = self.executor_server._getMerger(
                        root,
                        self.jobdir.src_root,
                        self.log)
                    break

            if merger is None:
                merger = self.executor_server._getMerger(
                    root,
                    self.executor_server.merge_root,
                    self.log)

            self.log.debug("Cloning %s@%s into new untrusted space %s",
                           project, branch, root)
            merger.checkoutBranch(project.connection_name, project.name,
                                  branch)
        else:
            self.log.debug("Using existing repo %s@%s in trusted space %s",
                           project, branch, root)

        path = os.path.join(root,
                            project.canonical_hostname,
                            project.name)
        return path

    def prepareRole(self, jobdir_playbook, role, args):
        if role['type'] == 'zuul':
            root = jobdir_playbook.addRole()
            self.prepareZuulRole(jobdir_playbook, role, args, root)

    def findRole(self, path, trusted=False):
        d = os.path.join(path, 'tasks')
        if os.path.isdir(d):
            # This is a bare role
            if not trusted:
                self._blockPluginDirs(path)
            # None signifies that the repo is a bare role
            return None
        d = os.path.join(path, 'roles')
        if os.path.isdir(d):
            # This repo has a collection of roles
            if not trusted:
                self._blockPluginDirs(d)
                for entry in os.listdir(d):
                    entry_path = os.path.join(d, entry)
                    if os.path.isdir(entry_path):
                        self._blockPluginDirs(entry_path)
            return d
        # It is neither a bare role, nor a collection of roles
        raise RoleNotFoundError("Unable to find role in %s" % (path,))

    def prepareZuulRole(self, jobdir_playbook, role, args, root):
        self.log.debug("Prepare zuul role for %s" % (role,))
        # Check out the role repo if needed
        source = self.executor_server.connections.getSource(
            role['connection'])
        project = source.getProject(role['project'])
        name = role['target_name']
        path = None

        # Find the branch to use for this role.  We should generally
        # follow the normal fallback procedure, unless this role's
        # project is the playbook's project, in which case we should
        # use the playbook branch.
        if jobdir_playbook.project_canonical_name == project.canonical_name:
            branch = jobdir_playbook.branch
            self.log.debug("Role project is playbook project, "
                           "using playbook branch %s", branch)
        else:
            # Find if the project is one of the job-specified projects.
            # If it is, we can honor the project checkout-override options.
            args_project = {}
            for p in args['projects']:
                if (p['canonical_name'] == project.canonical_name):
                    args_project = p
                    break

            branch, selected_desc = self.resolveBranch(
                project.canonical_name,
                None,
                args['branch'],
                args['override_branch'],
                args['override_checkout'],
                args_project.get('override_branch'),
                args_project.get('override_checkout'),
                role['project_default_branch'])
            self.log.debug("Role using %s %s", selected_desc, branch)

        if not jobdir_playbook.trusted:
            path = self.checkoutUntrustedProject(project, branch, args)
        else:
            path = self.checkoutTrustedProject(project, branch)

        # The name of the symlink is the requested name of the role
        # (which may be the repo name or may be something else; this
        # can come into play if this is a bare role).
        link = os.path.join(root, name)
        link = os.path.realpath(link)
        if not link.startswith(os.path.realpath(root)):
            raise ExecutorError("Invalid role name %s" % name)
        os.symlink(path, link)

        try:
            role_path = self.findRole(link, trusted=jobdir_playbook.trusted)
        except RoleNotFoundError:
            if role['implicit']:
                self.log.debug("Implicit role not found in %s", link)
                return
            raise
        except PluginFoundError:
            if role['implicit']:
                self.log.info("Not adding implicit role %s due to "
                              "plugin", link)
                return
            raise
        if role_path is None:
            # In the case of a bare role, add the containing directory
            role_path = root
        self.log.debug("Adding role path %s", role_path)
        jobdir_playbook.roles_path.append(role_path)

    def prepareKubeConfig(self, jobdir, data):
        kube_cfg_path = jobdir.kubeconfig
        if os.path.exists(kube_cfg_path):
            kube_cfg = yaml.safe_load(open(kube_cfg_path))
        else:
            kube_cfg = {
                'apiVersion': 'v1',
                'kind': 'Config',
                'preferences': {},
                'users': [],
                'clusters': [],
                'contexts': [],
                'current-context': None,
            }
        # Add cluster
        cluster_name = urlsplit(data['host']).netloc.replace('.', '-')

        # Do not add a cluster/server that already exists in the kubeconfig
        # because that leads to 'duplicate name' errors on multi-node builds.
        # Also, as the cluster name directly corresponds to a server, there
        # is no need to add it twice.
        if cluster_name not in [c['name'] for c in kube_cfg['clusters']]:
            cluster = {
                'server': data['host'],
            }
            if data.get('ca_crt'):
                cluster['certificate-authority-data'] = data['ca_crt']
            if data['skiptls']:
                cluster['insecure-skip-tls-verify'] = True
            kube_cfg['clusters'].append({
                'name': cluster_name,
                'cluster': cluster,
            })

        # Add user
        user_name = "%s:%s" % (data['namespace'], data['user'])
        kube_cfg['users'].append({
            'name': user_name,
            'user': {
                'token': data['token'],
            },
        })

        # Add context
        data['context_name'] = "%s/%s" % (user_name, cluster_name)
        kube_cfg['contexts'].append({
            'name': data['context_name'],
            'context': {
                'user': user_name,
                'cluster': cluster_name,
                'namespace': data['namespace']
            }
        })
        if not kube_cfg['current-context']:
            kube_cfg['current-context'] = data['context_name']

        with open(kube_cfg_path, "w") as of:
            of.write(yaml.safe_dump(kube_cfg, default_flow_style=False))

    def prepareAnsibleFiles(self, args):
        all_vars = args['vars'].copy()
        check_varnames(all_vars)
        all_vars['zuul'] = args['zuul'].copy()
        all_vars['zuul']['executor'] = dict(
            hostname=self.executor_server.hostname,
            src_root=self.jobdir.src_root,
            log_root=self.jobdir.log_root,
            work_root=self.jobdir.work_root,
            result_data_file=self.jobdir.result_data_file,
            inventory_file=self.jobdir.inventory)

        resources_nodes = []
        all_vars['zuul']['resources'] = {}
        for node in args['nodes']:
            if node.get('connection_type') in (
                    'namespace', 'project', 'kubectl'):
                # TODO: decrypt resource data using scheduler key
                data = node['connection_port']
                # Setup kube/config file
                self.prepareKubeConfig(self.jobdir, data)
                # Convert connection_port in kubectl connection parameters
                node['connection_port'] = None
                node['kubectl_namespace'] = data['namespace']
                node['kubectl_context'] = data['context_name']
                # Add node information to zuul_resources
                all_vars['zuul']['resources'][node['name'][0]] = {
                    'namespace': data['namespace'],
                    'context': data['context_name'],
                }
                if node['connection_type'] in ('project', 'namespace'):
                    # Project are special nodes that are not the inventory
                    resources_nodes.append(node)
                else:
                    # Add the real pod name to the resources_var
                    all_vars['zuul']['resources'][
                        node['name'][0]]['pod'] = data['pod']
                    fwd = KubeFwd(zuul_event_id=self.zuul_event_id,
                                  build=self.job.unique,
                                  kubeconfig=self.jobdir.kubeconfig,
                                  context=data['context_name'],
                                  namespace=data['namespace'],
                                  pod=data['pod'])
                    try:
                        fwd.start()
                        self.port_forwards.append(fwd)
                        all_vars['zuul']['resources'][
                            node['name'][0]]['stream_port'] = fwd.port
                    except Exception:
                        self.log.exception("Unable to start port forward:")
                        self.log.error("Kubectl and socat are required for "
                                       "streaming logs")

        # Remove resource node from nodes list
        for node in resources_nodes:
            args['nodes'].remove(node)

        nodes = self.getHostList(args)
        setup_inventory = make_setup_inventory_dict(nodes)
        inventory = make_inventory_dict(nodes, args, all_vars)

        with open(self.jobdir.setup_inventory, 'w') as setup_inventory_yaml:
            setup_inventory_yaml.write(
                yaml.safe_dump(setup_inventory, default_flow_style=False))

        with open(self.jobdir.inventory, 'w') as inventory_yaml:
            inventory_yaml.write(
                yaml.safe_dump(inventory, default_flow_style=False))

        with open(self.jobdir.known_hosts, 'w') as known_hosts:
            for node in nodes:
                for key in node['host_keys']:
                    known_hosts.write('%s\n' % key)

        with open(self.jobdir.extra_vars, 'w') as extra_vars:
            extra_vars.write(
                yaml.safe_dump(args['extra_vars'], default_flow_style=False))

    def writeLoggingConfig(self):
        self.log.debug("Writing logging config for job %s %s",
                       self.jobdir.job_output_file,
                       self.jobdir.logging_json)
        logging_config = zuul.ansible.logconfig.JobLoggingConfig(
            job_output_file=self.jobdir.job_output_file)
        logging_config.writeJson(self.jobdir.logging_json)

    def writeAnsibleConfig(self, jobdir_playbook):
        trusted = jobdir_playbook.trusted

        # TODO(mordred) This should likely be extracted into a more generalized
        #               mechanism for deployers being able to add callback
        #               plugins.
        if self.ara_callbacks:
            callback_path = '%s:%s' % (
                self.callback_dir,
                os.path.dirname(self.ara_callbacks))
        else:
            callback_path = self.callback_dir
        with open(jobdir_playbook.ansible_config, 'w') as config:
            config.write('[defaults]\n')
            config.write('inventory = %s\n' % self.jobdir.inventory)
            config.write('local_tmp = %s\n' % self.jobdir.local_tmp)
            config.write('retry_files_enabled = False\n')
            config.write('gathering = smart\n')
            config.write('fact_caching = jsonfile\n')
            config.write('fact_caching_connection = %s\n' %
                         self.jobdir.fact_cache)
            config.write('library = %s\n'
                         % self.library_dir)
            config.write('command_warnings = False\n')
            config.write('callback_plugins = %s\n' % callback_path)
            config.write('stdout_callback = zuul_stream\n')
            config.write('filter_plugins = %s\n'
                         % self.filter_dir)
            config.write('nocows = True\n')  # save useless stat() calls
            # bump the timeout because busy nodes may take more than
            # 10s to respond
            config.write('timeout = 30\n')

            # We need the general action dir to make the zuul_return plugin
            # available to every job.
            action_dirs = [self.action_dir_general]
            if not trusted:
                # Untrusted jobs add the action dir which makes sure localhost
                # modules are restricted where needed. Further the command
                # plugin needs to be restricted and also inject zuul_log_id
                # to make log streaming work.
                action_dirs.append(self.action_dir)
                config.write('lookup_plugins = %s\n'
                             % self.lookup_dir)
            else:
                # Trusted jobs add the actiontrusted dir which adds the
                # unrestricted command plugin to inject zuul_log_id to make
                # log streaming work.
                action_dirs.append(self.action_dir_trusted)

            config.write('action_plugins = %s\n'
                         % ':'.join(action_dirs))

            if jobdir_playbook.roles_path:
                config.write('roles_path = %s\n' % ':'.join(
                    jobdir_playbook.roles_path))

            # On playbooks with secrets we want to prevent the
            # printing of args since they may be passed to a task or a
            # role. Otherwise, printing the args could be useful for
            # debugging.
            config.write('display_args_to_stdout = %s\n' %
                         str(not jobdir_playbook.secrets_content))

            # Increase the internal poll interval of ansible.
            # The default interval of 0.001s is optimized for interactive
            # ui at the expense of CPU load. As we have a non-interactive
            # automation use case a longer poll interval is more suitable
            # and reduces CPU load of the ansible process.
            config.write('internal_poll_interval = 0.01\n')

            if self.ansible_callbacks:
                config.write('callback_whitelist =\n')
                for callback in self.ansible_callbacks.keys():
                    config.write('    %s,\n' % callback)

            config.write('[ssh_connection]\n')
            # NOTE(pabelanger): Try up to 3 times to run a task on a host, this
            # helps to mitigate UNREACHABLE host errors with SSH.
            config.write('retries = 3\n')
            # NB: when setting pipelining = True, keep_remote_files
            # must be False (the default).  Otherwise it apparently
            # will override the pipelining option and effectively
            # disable it.  Pipelining has a side effect of running the
            # command without a tty (ie, without the -tt argument to
            # ssh).  We require this behavior so that if a job runs a
            # command which expects interactive input on a tty (such
            # as sudo) it does not hang.
            config.write('pipelining = True\n')
            config.write('control_path_dir = %s\n' % self.jobdir.control_path)
            ssh_args = "-o ControlMaster=auto -o ControlPersist=60s " \
                "-o ServerAliveInterval=60 " \
                "-o UserKnownHostsFile=%s" % self.jobdir.known_hosts
            config.write('ssh_args = %s\n' % ssh_args)

            if self.ansible_callbacks:
                for cb_name, cb_config in self.ansible_callbacks.items():
                    config.write("[callback_%s]\n" % cb_name)
                    for k, n in cb_config.items():
                        config.write("%s = %s\n" % (k, n))

    def _ansibleTimeout(self, msg):
        self.log.warning(msg)
        self.abortRunningProc()

    def abortRunningProc(self):
        with self.proc_lock:
            if self.proc and not self.cleanup_started:
                self.log.debug("Abort: sending kill signal to job "
                               "process group")
                try:
                    pgid = os.getpgid(self.proc.pid)
                    os.killpg(pgid, signal.SIGKILL)
                except Exception:
                    self.log.exception(
                        "Exception while killing ansible process:")
            elif self.proc and self.cleanup_started:
                self.log.debug("Abort: cleanup is in progress")
            else:
                self.log.debug("Abort: no process is running")

    def runAnsible(self, cmd, timeout, playbook, ansible_version,
                   wrapped=True, cleanup=False):
        config_file = playbook.ansible_config
        env_copy = {key: value
                    for key, value in os.environ.copy().items()
                    if not key.startswith("ZUUL_")}
        env_copy.update(self.ssh_agent.env)
        if self.ara_callbacks:
            env_copy['ARA_LOG_CONFIG'] = self.jobdir.logging_json
        env_copy['ZUUL_JOB_LOG_CONFIG'] = self.jobdir.logging_json
        env_copy['ZUUL_JOBDIR'] = self.jobdir.root
        if self.executor_server.log_console_port != DEFAULT_STREAM_PORT:
            env_copy['ZUUL_CONSOLE_PORT'] = str(
                self.executor_server.log_console_port)
        env_copy['TMP'] = self.jobdir.local_tmp
        pythonpath = env_copy.get('PYTHONPATH')
        if pythonpath:
            pythonpath = [pythonpath]
        else:
            pythonpath = []

        ansible_dir = self.executor_server.ansible_manager.getAnsibleDir(
            ansible_version)
        pythonpath = [ansible_dir] + pythonpath
        env_copy['PYTHONPATH'] = os.path.pathsep.join(pythonpath)

        if playbook.trusted:
            opt_prefix = 'trusted'
        else:
            opt_prefix = 'untrusted'
        ro_paths = get_default(self.executor_server.config, 'executor',
                               '%s_ro_paths' % opt_prefix)
        rw_paths = get_default(self.executor_server.config, 'executor',
                               '%s_rw_paths' % opt_prefix)
        ro_paths = ro_paths.split(":") if ro_paths else []
        rw_paths = rw_paths.split(":") if rw_paths else []

        ro_paths.append(ansible_dir)
        ro_paths.append(
            self.executor_server.ansible_manager.getAnsibleInstallDir(
                ansible_version))
        ro_paths.append(self.jobdir.ansible_root)
        ro_paths.append(self.jobdir.trusted_root)
        ro_paths.append(self.jobdir.untrusted_root)
        ro_paths.append(playbook.root)

        rw_paths.append(self.jobdir.ansible_cache_root)

        if self.executor_variables_file:
            ro_paths.append(self.executor_variables_file)

        secrets = {}
        if playbook.secrets_content:
            secrets[playbook.secrets] = playbook.secrets_content

        if wrapped:
            wrapper = self.executor_server.execution_wrapper
        else:
            wrapper = self.executor_server.connections.drivers['nullwrap']

        context = wrapper.getExecutionContext(ro_paths, rw_paths, secrets)

        popen = context.getPopen(
            work_dir=self.jobdir.work_root,
            ssh_auth_sock=env_copy.get('SSH_AUTH_SOCK'))

        env_copy['ANSIBLE_CONFIG'] = config_file
        # NOTE(pabelanger): Default HOME variable to jobdir.work_root, as it is
        # possible we don't bind mount current zuul user home directory.
        env_copy['HOME'] = self.jobdir.work_root

        with self.proc_lock:
            if self.aborted and not cleanup:
                return (self.RESULT_ABORTED, None)
            self.log.debug("Ansible command: ANSIBLE_CONFIG=%s ZUUL_JOBDIR=%s "
                           "ZUUL_JOB_LOG_CONFIG=%s PYTHONPATH=%s TMP=%s %s",
                           env_copy['ANSIBLE_CONFIG'],
                           env_copy['ZUUL_JOBDIR'],
                           env_copy['ZUUL_JOB_LOG_CONFIG'],
                           env_copy['PYTHONPATH'],
                           env_copy['TMP'],
                           " ".join(shlex.quote(c) for c in cmd))
            self.proc = popen(
                cmd,
                cwd=self.jobdir.work_root,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                start_new_session=True,
                env=env_copy,
            )

        syntax_buffer = []
        ret = None
        if timeout:
            watchdog = Watchdog(timeout, self._ansibleTimeout,
                                ("Ansible timeout exceeded: %s" % timeout,))
            watchdog.start()
        try:
            ansible_log = get_annotated_logger(
                logging.getLogger("zuul.AnsibleJob.output"),
                self.zuul_event_id, build=self.job.unique)

            # Use manual idx instead of enumerate so that RESULT lines
            # don't count towards BUFFER_LINES_FOR_SYNTAX
            idx = 0
            for line in iter(self.proc.stdout.readline, b''):
                if line.startswith(b'RESULT'):
                    # TODO(mordred) Process result commands if sent
                    continue
                else:
                    idx += 1
                if idx < BUFFER_LINES_FOR_SYNTAX:
                    syntax_buffer.append(line)
                line = line[:1024].rstrip()
                ansible_log.debug("Ansible output: %s" % (line,))
            self.log.debug("Ansible output terminated")
            try:
                cpu_times = self.proc.cpu_times()
                self.log.debug("Ansible cpu times: user=%.2f, system=%.2f, "
                               "children_user=%.2f, "
                               "children_system=%.2f" %
                               (cpu_times.user, cpu_times.system,
                                cpu_times.children_user,
                                cpu_times.children_system))
                self.cpu_times['user'] += cpu_times.user
                self.cpu_times['system'] += cpu_times.system
                self.cpu_times['children_user'] += cpu_times.children_user
                self.cpu_times['children_system'] += cpu_times.children_system
            except psutil.NoSuchProcess:
                self.log.warn("Cannot get cpu_times for process %d. Is your"
                              "/proc mounted with hidepid=2"
                              " on an old linux kernel?", self.proc.pid)
            ret = self.proc.wait()
            self.log.debug("Ansible exit code: %s" % (ret,))
        finally:
            if timeout:
                watchdog.stop()
                self.log.debug("Stopped watchdog")
            self.log.debug("Stopped disk job killer")

        with self.proc_lock:
            self.proc.stdout.close()
            self.proc = None

        if timeout and watchdog.timed_out:
            return (self.RESULT_TIMED_OUT, None)
        # Note: Unlike documented ansible currently wrongly returns 4 on
        # unreachable so we have the zuul_unreachable callback module that
        # creates the file job-output.unreachable in case there were
        # unreachable nodes. This can be removed once ansible returns a
        # distinct value for unreachable.
        if ret == 3 or os.path.exists(self.jobdir.job_unreachable_file):
            # AnsibleHostUnreachable: We had a network issue connecting to
            # our zuul-worker.
            return (self.RESULT_UNREACHABLE, None)
        elif ret == -9:
            # Received abort request.
            return (self.RESULT_ABORTED, None)
        elif ret == 1:
            with open(self.jobdir.job_output_file, 'a') as job_output:
                found_marker = False
                for line in syntax_buffer:
                    if line.startswith(b'ERROR!'):
                        found_marker = True
                    if not found_marker:
                        continue
                    job_output.write("{now} | {line}\n".format(
                        now=datetime.datetime.now(),
                        line=line.decode('utf-8').rstrip()))
        elif ret == 4:
            # Ansible could not parse the yaml.
            self.log.debug("Ansible parse error")
            # TODO(mordred) If/when we rework use of logger in ansible-playbook
            # we'll want to change how this works to use that as well. For now,
            # this is what we need to do.
            # TODO(mordred) We probably want to put this into the json output
            # as well.
            with open(self.jobdir.job_output_file, 'a') as job_output:
                job_output.write("{now} | ANSIBLE PARSE ERROR\n".format(
                    now=datetime.datetime.now()))
                for line in syntax_buffer:
                    job_output.write("{now} | {line}\n".format(
                        now=datetime.datetime.now(),
                        line=line.decode('utf-8').rstrip()))
        elif ret == 250:
            # Unexpected error from ansible
            with open(self.jobdir.job_output_file, 'a') as job_output:
                job_output.write("{now} | UNEXPECTED ANSIBLE ERROR\n".format(
                    now=datetime.datetime.now()))
                found_marker = False
                for line in syntax_buffer:
                    if line.startswith(b'ERROR! Unexpected Exception'):
                        found_marker = True
                    if not found_marker:
                        continue
                    job_output.write("{now} | {line}\n".format(
                        now=datetime.datetime.now(),
                        line=line.decode('utf-8').rstrip()))
        elif ret == 2:
            with open(self.jobdir.job_output_file, 'a') as job_output:
                found_marker = False
                for line in syntax_buffer:
                    # This is a workaround to detect winrm connection failures
                    # that are not detected by ansible. These can be detected
                    # if the string 'FATAL ERROR DURING FILE TRANSFER' is in
                    # the ansible output. In this case we should treat the
                    # host as unreachable and retry the job.
                    if b'FATAL ERROR DURING FILE TRANSFER' in line:
                        return self.RESULT_UNREACHABLE, None

                    # Extract errors for special cases that are treated like
                    # task errors by Ansible (e.g. missing role when using
                    # 'include_role').
                    if line.startswith(b'ERROR!'):
                        found_marker = True
                    if not found_marker:
                        continue
                    job_output.write("{now} | {line}\n".format(
                        now=datetime.datetime.now(),
                        line=line.decode('utf-8').rstrip()))

        if self.aborted:
            return (self.RESULT_ABORTED, None)

        return (self.RESULT_NORMAL, ret)

    def runAnsibleSetup(self, playbook, ansible_version):
        if self.executor_server.verbose:
            verbose = '-vvv'
        else:
            verbose = '-v'

        # TODO: select correct ansible version from job
        ansible = self.executor_server.ansible_manager.getAnsibleCommand(
            ansible_version,
            command='ansible')
        cmd = [ansible, '*', verbose, '-m', 'setup',
               '-i', self.jobdir.setup_inventory,
               '-a', 'gather_subset=!all']
        if self.executor_variables_file is not None:
            cmd.extend(['-e@%s' % self.executor_variables_file])

        result, code = self.runAnsible(
            cmd=cmd, timeout=self.executor_server.setup_timeout,
            playbook=playbook, ansible_version=ansible_version, wrapped=False)
        self.log.debug("Ansible complete, result %s code %s" % (
            self.RESULT_MAP[result], code))
        if self.executor_server.statsd:
            base_key = "zuul.executor.{hostname}.phase.setup"
            self.executor_server.statsd.incr(base_key + ".%s" %
                                             self.RESULT_MAP[result])
        return result, code

    def runAnsibleCleanup(self, playbook):
        # TODO(jeblair): This requires a bugfix in Ansible 2.4
        # Once this is used, increase the controlpersist timeout.
        return (self.RESULT_NORMAL, 0)

        if self.executor_server.verbose:
            verbose = '-vvv'
        else:
            verbose = '-v'

        cmd = ['ansible', '*', verbose, '-m', 'meta',
               '-a', 'reset_connection']

        result, code = self.runAnsible(
            cmd=cmd, timeout=60, playbook=playbook,
            wrapped=False)
        self.log.debug("Ansible complete, result %s code %s" % (
            self.RESULT_MAP[result], code))
        if self.executor_server.statsd:
            base_key = "zuul.executor.{hostname}.phase.cleanup"
            self.executor_server.statsd.incr(base_key + ".%s" %
                                             self.RESULT_MAP[result])
        return result, code

    def emitPlaybookBanner(self, playbook, step, phase, result=None):
        # This is used to print a header and a footer, respectively at the
        # beginning and the end of each playbook execution.
        # We are doing it from the executor rather than from a callback because
        # the parameters are not made available to the callback until it's too
        # late.
        phase = phase or ''
        trusted = playbook.trusted
        trusted = 'trusted' if trusted else 'untrusted'
        branch = playbook.branch
        playbook = playbook.canonical_name_and_path

        if phase and phase != 'run':
            phase = '{phase}-run'.format(phase=phase)
        phase = phase.upper()

        if result is not None:
            result = self.RESULT_MAP[result]
            msg = "{phase} {step} {result}: [{trusted} : {playbook}@{branch}]"
            msg = msg.format(phase=phase, step=step, result=result,
                             trusted=trusted, playbook=playbook, branch=branch)
        else:
            msg = "{phase} {step}: [{trusted} : {playbook}@{branch}]"
            msg = msg.format(phase=phase, step=step, trusted=trusted,
                             playbook=playbook, branch=branch)

        with open(self.jobdir.job_output_file, 'a') as job_output:
            job_output.write("{now} | {msg}\n".format(
                now=datetime.datetime.now(),
                msg=msg))

    def runAnsiblePlaybook(self, playbook, timeout, ansible_version,
                           success=None, phase=None, index=None):
        if self.executor_server.verbose:
            verbose = '-vvv'
        else:
            verbose = '-v'

        cmd = [self.executor_server.ansible_manager.getAnsibleCommand(
            ansible_version), verbose, playbook.path]
        if playbook.secrets_content:
            cmd.extend(['-e', '@' + playbook.secrets])

        cmd.extend(['-e', '@' + self.jobdir.extra_vars])

        if success is not None:
            cmd.extend(['-e', 'zuul_success=%s' % str(bool(success))])

        if phase:
            cmd.extend(['-e', 'zuul_execution_phase=%s' % phase])

        if index is not None:
            cmd.extend(['-e', 'zuul_execution_phase_index=%s' % index])

        cmd.extend(['-e', 'zuul_execution_trusted=%s' % str(playbook.trusted)])
        cmd.extend([
            '-e',
            'zuul_execution_canonical_name_and_path=%s'
            % playbook.canonical_name_and_path])
        cmd.extend(['-e', 'zuul_execution_branch=%s' % str(playbook.branch)])

        if self.executor_variables_file is not None:
            cmd.extend(['-e@%s' % self.executor_variables_file])

        if not playbook.trusted:
            cmd.extend(['-e', '@' + self.jobdir.ansible_vars_blacklist])

        self.emitPlaybookBanner(playbook, 'START', phase)

        result, code = self.runAnsible(cmd, timeout, playbook, ansible_version,
                                       cleanup=phase == 'cleanup')
        self.log.debug("Ansible complete, result %s code %s" % (
            self.RESULT_MAP[result], code))
        if self.executor_server.statsd:
            base_key = "zuul.executor.{hostname}.phase.{phase}"
            self.executor_server.statsd.incr(
                base_key + ".{result}",
                result=self.RESULT_MAP[result],
                phase=phase or 'unknown')

        self.emitPlaybookBanner(playbook, 'END', phase, result=result)
        return result, code


class ExecutorMergeWorker(gear.TextWorker):
    def __init__(self, executor_server, *args, **kw):
        self.zuul_executor_server = executor_server
        super(ExecutorMergeWorker, self).__init__(*args, **kw)

    def handleNoop(self, packet):
        # Wait until the update queue is empty before responding
        while self.zuul_executor_server.update_queue.qsize():
            time.sleep(1)

        super(ExecutorMergeWorker, self).handleNoop(packet)


class ExecutorExecuteWorker(gear.TextWorker):
    def __init__(self, executor_server, *args, **kw):
        self.zuul_executor_server = executor_server
        super(ExecutorExecuteWorker, self).__init__(*args, **kw)

    def handleNoop(self, packet):
        # Delay our response to running a new job based on the number
        # of jobs we're currently running, in an attempt to spread
        # load evenly among executors.
        workers = len(self.zuul_executor_server.job_workers)
        delay = (workers ** 2) / 1000.0
        time.sleep(delay)
        return super(ExecutorExecuteWorker, self).handleNoop(packet)


class ExecutorServer(BaseMergeServer):
    log = logging.getLogger("zuul.ExecutorServer")
    _ansible_manager_class = AnsibleManager
    _job_class = AnsibleJob
    _repo_locks_class = RepoLocks

    def __init__(
        self,
        config,
        connections=None,
        jobdir_root=None,
        keep_jobdir=False,
        log_streaming_port=DEFAULT_FINGER_PORT,
        log_console_port=DEFAULT_STREAM_PORT,
    ):
        super().__init__(config, 'executor', connections)

        self.keep_jobdir = keep_jobdir
        self.jobdir_root = jobdir_root
        # TODOv3(mordred): make the executor name more unique --
        # perhaps hostname+pid.
        self.hostname = get_default(self.config, 'executor', 'hostname',
                                    socket.getfqdn())
        self.zk_component = self.zk_component_registry.register(
            'executors', self.hostname
        )
        self.log_streaming_port = log_streaming_port
        self.governor_lock = threading.Lock()
        self.run_lock = threading.Lock()
        self.verbose = False
        self.command_map = dict(
            stop=self.stop,
            pause=self.pause,
            unpause=self.unpause,
            graceful=self.graceful,
            verbose=self.verboseOn,
            unverbose=self.verboseOff,
            keep=self.keep,
            nokeep=self.nokeep,
            repl=self.start_repl,
            norepl=self.stop_repl,
        )
        self.log_console_port = log_console_port
        self.repl = None

        statsd_extra_keys = {'hostname': self.hostname}
        self.statsd = get_statsd(config, statsd_extra_keys)
        self.default_username = get_default(self.config, 'executor',
                                            'default_username', 'zuul')
        self.disk_limit_per_job = int(get_default(self.config, 'executor',
                                                  'disk_limit_per_job', 250))
        self.setup_timeout = int(get_default(self.config, 'executor',
                                             'ansible_setup_timeout', 60))
        self.zone = get_default(self.config, 'executor', 'zone')
        self.allow_unzoned = get_default(self.config, 'executor',
                                         'allow_unzoned', False)

        self.ansible_callbacks = {}
        for section_name in self.config.sections():
            cb_match = re.match(r'^ansible_callback ([\'\"]?)(.*)(\1)$',
                                section_name, re.I)
            if not cb_match:
                continue
            cb_name = cb_match.group(2)
            self.ansible_callbacks[cb_name] = dict(
                self.config.items(section_name)
            )

        # TODO(tobiash): Take cgroups into account
        self.update_workers = multiprocessing.cpu_count()
        self.update_threads = []
        # If the execution driver ever becomes configurable again,
        # this is where it would happen.
        execution_wrapper_name = 'bubblewrap'
        self.accepting_work = False
        self.execution_wrapper = connections.drivers[execution_wrapper_name]

        self.update_queue = DeduplicateQueue()

        command_socket = get_default(
            self.config, 'executor', 'command_socket',
            '/var/lib/zuul/executor.socket')
        self.command_socket = commandsocket.CommandSocket(command_socket)

        state_dir = get_default(self.config, 'executor', 'state_dir',
                                '/var/lib/zuul', expand_user=True)

        # If keep is not set, ensure the job dir is empty on startup,
        # in case we were uncleanly shut down.
        if not self.keep_jobdir:
            for fn in os.listdir(self.jobdir_root):
                fn = os.path.join(self.jobdir_root, fn)
                if not os.path.isdir(fn):
                    continue
                self.log.info("Deleting stale jobdir %s", fn)
                # We use rm here instead of shutil because of
                # https://bugs.python.org/issue22040
                jobdir = os.path.join(self.jobdir_root, fn)
                # First we need to ensure all directories are
                # writable to avoid permission denied error
                subprocess.Popen([
                    "find", jobdir,
                    # Filter non writable perms
                    "-type", "d", "!", "-perm", "/u+w",
                    # Replace by writable perms
                    "-exec", "chmod", "0700", "{}", "+"]).wait()
                if subprocess.Popen(["rm", "-Rf", jobdir]).wait():
                    raise RuntimeError("Couldn't delete: " + jobdir)

        self.job_workers = {}
        self.disk_accountant = DiskAccountant(self.jobdir_root,
                                              self.disk_limit_per_job,
                                              self.stopJobDiskFull,
                                              self.merge_root)

        self.pause_sensor = PauseSensor(get_default(self.config, 'executor',
                                                    'paused_on_start', False))
        self.log.info("Starting executor (hostname: %s) in %spaused mode" % (
            self.hostname, "" if self.pause_sensor.pause else "un"))
        cpu_sensor = CPUSensor(config)
        self.sensors = [
            cpu_sensor,
            HDDSensor(config),
            self.pause_sensor,
            RAMSensor(config),
            StartingBuildsSensor(self, cpu_sensor.max_load_avg, config)
        ]

        manage_ansible = get_default(
            self.config, 'executor', 'manage_ansible', True)
        ansible_dir = os.path.join(state_dir, 'ansible')
        ansible_install_root = get_default(
            self.config, 'executor', 'ansible_root', None)
        if not ansible_install_root:
            # NOTE: Even though we set this value the zuul installation
            # adjacent virtualenv location is still checked by the ansible
            # manager. ansible_install_root's value is only used if those
            # default locations do not have venvs preinstalled.
            ansible_install_root = os.path.join(state_dir, 'ansible-bin')
        self.ansible_manager = self._ansible_manager_class(
            ansible_dir, runtime_install_root=ansible_install_root)
        if not self.ansible_manager.validate():
            if not manage_ansible:
                raise Exception('Error while validating ansible '
                                'installations. Please run '
                                'zuul-manage-ansible to install all supported '
                                'ansible versions.')
            else:
                self.ansible_manager.install()
        self.ansible_manager.copyAnsibleFiles()

        self.process_merge_jobs = get_default(self.config, 'executor',
                                              'merge_jobs', True)

        self.executor_jobs = {
            "executor:resume:%s" % self.hostname: self.resumeJob,
            "executor:stop:%s" % self.hostname: self.stopJob,
        }
        for function_name in self._getExecuteFunctionNames():
            self.executor_jobs[function_name] = self.executeJob
        for function_name in self._getOnlineFunctionNames():
            self.executor_jobs[function_name] = self.noop

        self.executor_gearworker = ZuulGearWorker(
            'Zuul Executor Server',
            'zuul.ExecutorServer.ExecuteWorker',
            'executor',
            self.config,
            self.executor_jobs,
            worker_class=ExecutorExecuteWorker,
            worker_args=[self])

        # Used to offload expensive operations to different processes
        self.process_worker = None

    def _getFunctionSuffixes(self):
        suffixes = []
        if self.zone:
            suffixes.append(':' + self.zone)
            if self.allow_unzoned:
                suffixes.append('')
        else:
            suffixes.append('')
        return suffixes

    def _getExecuteFunctionNames(self):
        base_name = 'executor:execute'
        return [base_name + suffix for suffix in self._getFunctionSuffixes()]

    def _getOnlineFunctionNames(self):
        base_name = 'executor:online'
        return [base_name + suffix for suffix in self._getFunctionSuffixes()]

    def _repoLock(self, connection_name, project_name):
        return self.repo_locks.getRepoLock(connection_name, project_name)

    def noop(self, job):
        """A noop gearman job so we can register for statistics."""
        job.sendWorkComplete()

    def start(self):
        # Start merger worker only if we process merge jobs
        if self.process_merge_jobs:
            super().start()

        self._running = True
        self._command_running = True

        try:
            multiprocessing.set_start_method('spawn')
        except RuntimeError:
            # Note: During tests this can be called multiple times which
            # results in a runtime error. This is ok here as we've set this
            # already correctly.
            self.log.warning('Multiprocessing context has already been set')
        self.process_worker = ProcessPoolExecutor()

        self.executor_gearworker.start()

        self.log.debug("Starting command processor")
        self.command_socket.start()
        self.command_thread = threading.Thread(target=self.runCommand,
                                               name='command')
        self.command_thread.daemon = True
        self.command_thread.start()

        self.log.debug("Starting %s update workers" % self.update_workers)
        for i in range(self.update_workers):
            update_thread = threading.Thread(target=self._updateLoop,
                                             name='update')
            update_thread.daemon = True
            update_thread.start()
            self.update_threads.append(update_thread)

        self.governor_stop_event = threading.Event()
        self.governor_thread = threading.Thread(target=self.run_governor,
                                                name='governor')
        self.governor_thread.daemon = True
        self.governor_thread.start()
        self.disk_accountant.start()
        self.zk_component.set('state', self.zk_component.RUNNING)

    def register_work(self):
        if self._running:
            self.accepting_work = True
            for function in self._getExecuteFunctionNames():
                self.executor_gearworker.gearman.registerFunction(function)
            # TODO(jeblair): Update geard to send a noop after
            # registering for a job which is in the queue, then remove
            # this API violation.
            self.executor_gearworker.gearman._sendGrabJobUniq()

    def unregister_work(self):
        self.accepting_work = False
        for function in self._getExecuteFunctionNames():
            self.executor_gearworker.gearman.unRegisterFunction(function)

    def stop(self):
        self.log.debug("Stopping")
        self.zk_component.set('state', self.zk_component.STOPPED)
        # Use the BaseMergeServer's stop method to disconnect from ZooKeeper.
        super().stop()
        self.connections.stop()
        self.disk_accountant.stop()
        # The governor can change function registration, so make sure
        # it has stopped.
        self.governor_stop_event.set()
        self.governor_thread.join()
        # Stop accepting new jobs
        if self.merger_gearworker is not None:
            self.merger_gearworker.gearman.setFunctions([])
        self.executor_gearworker.gearman.setFunctions([])
        # Tell the executor worker to abort any jobs it just accepted,
        # and grab the list of currently running job workers.
        with self.run_lock:
            self._running = False
            self._command_running = False
            workers = list(self.job_workers.values())

        for job_worker in workers:
            try:
                job_worker.stop()
            except Exception:
                self.log.exception("Exception sending stop command "
                                   "to worker:")
        for job_worker in workers:
            try:
                job_worker.wait()
            except Exception:
                self.log.exception("Exception waiting for worker "
                                   "to stop:")

        # Now that we aren't accepting any new jobs, and all of the
        # running jobs have stopped, tell the update processor to
        # stop.
        for _ in self.update_threads:
            self.update_queue.put(None)

        self.command_socket.stop()

        # All job results should have been sent by now, shutdown the
        # gearman workers.
        self.executor_gearworker.stop()

        if self.process_worker is not None:
            self.process_worker.shutdown()

        if self.statsd:
            base_key = 'zuul.executor.{hostname}'
            self.statsd.gauge(base_key + '.load_average', 0)
            self.statsd.gauge(base_key + '.pct_used_ram', 0)
            self.statsd.gauge(base_key + '.running_builds', 0)

        self.stop_repl()
        self.log.debug("Stopped")

    def join(self):
        self.governor_thread.join()
        for update_thread in self.update_threads:
            update_thread.join()
        if self.process_merge_jobs:
            super().join()
        self.executor_gearworker.join()
        self.command_thread.join()

    def pause(self):
        self.log.debug('Pausing')
        self.zk_component.set('state', self.zk_component.PAUSED)
        self.pause_sensor.pause = True
        if self.process_merge_jobs:
            super().pause()

    def unpause(self):
        self.log.debug('Resuming')
        self.zk_component.set('state', self.zk_component.RUNNING)
        self.pause_sensor.pause = False
        if self.process_merge_jobs:
            super().unpause()

    def graceful(self):
        # This pauses the executor end shuts it down when there is no running
        # build left anymore
        self.log.info('Stopping graceful')
        self.pause()
        while self.job_workers:
            self.log.debug('Waiting for %s jobs to end', len(self.job_workers))
            time.sleep(30)
        try:
            self.stop()
        except Exception:
            self.log.exception('Error while stopping')

    def verboseOn(self):
        self.verbose = True

    def verboseOff(self):
        self.verbose = False

    def keep(self):
        self.keep_jobdir = True

    def nokeep(self):
        self.keep_jobdir = False

    def start_repl(self):
        if self.repl:
            return
        self.repl = zuul.lib.repl.REPLServer(self)
        self.repl.start()

    def stop_repl(self):
        if not self.repl:
            # not running
            return
        self.repl.stop()
        self.repl = None

    def runCommand(self):
        while self._command_running:
            try:
                command = self.command_socket.get().decode('utf8')
                if command != '_stop':
                    self.command_map[command]()
            except Exception:
                self.log.exception("Exception while processing command")

    def _updateLoop(self):
        while True:
            try:
                self._innerUpdateLoop()
            except StopException:
                return
            except Exception:
                self.log.exception("Exception in update thread:")

    def resetProcessPool(self):
        """
        This is called in order to re-initialize a broken process pool if it
        got broken e.g. by an oom killed child process
        """
        if self.process_worker:
            try:
                self.process_worker.shutdown()
            except Exception:
                self.log.exception('Failed to shutdown broken process worker')
            self.process_worker = ProcessPoolExecutor()

    def _innerUpdateLoop(self):
        # Inside of a loop that keeps the main repositories up to date
        task = self.update_queue.get()
        if task is None:
            # We are asked to stop
            raise StopException()
        log = get_annotated_logger(
            self.log, task.zuul_event_id, build=task.build)
        try:
            lock = self.repo_locks.getRepoLock(
                task.connection_name, task.project_name)
            with lock:
                log.info("Updating repo %s/%s",
                         task.connection_name, task.project_name)
                self.merger.updateRepo(
                    task.connection_name, task.project_name,
                    repo_state=task.repo_state,
                    zuul_event_id=task.zuul_event_id, build=task.build,
                    process_worker=self.process_worker)
                repo = self.merger.getRepo(
                    task.connection_name, task.project_name)
                source = self.connections.getSource(task.connection_name)
                project = source.getProject(task.project_name)
                task.canonical_name = project.canonical_name
                task.branches = repo.getBranches()
                task.refs = [r.name for r in repo.getRefs()]
                log.debug("Finished updating repo %s/%s",
                          task.connection_name, task.project_name)
                task.success = True
        except BrokenProcessPool:
            # The process pool got broken. Reset it to unbreak it for further
            # requests.
            log.exception('Process pool got broken')
            self.resetProcessPool()
        except Exception:
            log.exception('Got exception while updating repo %s/%s',
                          task.connection_name, task.project_name)
        finally:
            task.setComplete()

    def update(self, connection_name, project_name, repo_state=None,
               zuul_event_id=None, build=None):
        # Update a repository in the main merger

        state = None
        if repo_state:
            state = repo_state.get(connection_name, {}).get(project_name)

        task = UpdateTask(connection_name, project_name, repo_state=state,
                          zuul_event_id=zuul_event_id, build=build)
        task = self.update_queue.put(task)
        return task

    def _update(self, connection_name, project_name, zuul_event_id=None):
        """
        The executor overrides _update so it can do the update asynchronously.
        """
        log = get_annotated_logger(self.log, zuul_event_id)
        task = self.update(connection_name, project_name,
                           zuul_event_id=zuul_event_id)
        task.wait()
        if not task.success:
            msg = "Update of '{}' failed".format(project_name)
            log.error(msg)
            raise Exception(msg)

    def executeJob(self, job):
        args = json.loads(job.arguments)
        zuul_event_id = args.get('zuul_event_id')
        log = get_annotated_logger(self.log, zuul_event_id)
        log.debug("Got %s job: %s", job.name, job.unique)
        if self.statsd:
            base_key = 'zuul.executor.{hostname}'
            self.statsd.incr(base_key + '.builds')
        self.job_workers[job.unique] = self._job_class(self, job)
        # Run manageLoad before starting the thread mostly for the
        # benefit of the unit tests to make the calculation of the
        # number of starting jobs more deterministic.
        self.manageLoad()
        self.job_workers[job.unique].run()

    def run_governor(self):
        while not self.governor_stop_event.wait(10):
            try:
                self.manageLoad()
            except Exception:
                self.log.exception("Exception in governor thread:")

    def manageLoad(self):
        ''' Apply some heuristics to decide whether or not we should
            be asking for more jobs '''
        with self.governor_lock:
            return self._manageLoad()

    def _manageLoad(self):

        if self.accepting_work:
            # Don't unregister if we don't have any active jobs.
            for sensor in self.sensors:
                ok, message = sensor.isOk()
                if not ok:
                    self.log.info(
                        "Unregistering due to {}".format(message))
                    self.unregister_work()
                    break
        else:
            reregister = True
            limits = []
            for sensor in self.sensors:
                ok, message = sensor.isOk()
                limits.append(message)
                if not ok:
                    reregister = False
                    break
            if reregister:
                self.log.info("Re-registering as job is within its limits "
                              "{}".format(", ".join(limits)))
                self.register_work()
        if self.statsd:
            base_key = 'zuul.executor.{hostname}'
            for sensor in self.sensors:
                sensor.reportStats(self.statsd, base_key)

    def finishJob(self, unique):
        del(self.job_workers[unique])

    def stopJobDiskFull(self, jobdir):
        unique = os.path.basename(jobdir)
        self.stopJobByUnique(unique, reason=AnsibleJob.RESULT_DISK_FULL)

    def resumeJob(self, job):
        try:
            args = json.loads(job.arguments)
            zuul_event_id = args.get('zuul_event_id')
            log = get_annotated_logger(self.log, zuul_event_id)
            log.debug("Resume job with arguments: %s", args)
            unique = args['uuid']
            self.resumeJobByUnique(unique, zuul_event_id=zuul_event_id)
        finally:
            job.sendWorkComplete()

    def stopJob(self, job):
        try:
            args = json.loads(job.arguments)
            zuul_event_id = args.get('zuul_event_id')
            log = get_annotated_logger(self.log, zuul_event_id)
            log.debug("Stop job with arguments: %s", args)
            unique = args['uuid']
            self.stopJobByUnique(unique, zuul_event_id=zuul_event_id)
        finally:
            job.sendWorkComplete()

    def resumeJobByUnique(self, unique, zuul_event_id=None):
        log = get_annotated_logger(self.log, zuul_event_id)
        job_worker = self.job_workers.get(unique)
        if not job_worker:
            log.debug("Unable to find worker for job %s", unique)
            return
        try:
            job_worker.resume()
        except Exception:
            log.exception("Exception sending resume command to worker:")

    def stopJobByUnique(self, unique, reason=None, zuul_event_id=None):
        log = get_annotated_logger(self.log, zuul_event_id)
        job_worker = self.job_workers.get(unique)
        if not job_worker:
            log.debug("Unable to find worker for job %s", unique)
            return
        try:
            job_worker.stop(reason)
        except Exception:
            log.exception("Exception sending stop command to worker:")
