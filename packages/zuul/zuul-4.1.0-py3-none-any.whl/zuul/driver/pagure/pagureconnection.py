# Copyright 2018, 2019 Red Hat, Inc.
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

import logging
import hmac
import hashlib
import queue
import threading
import time
import re
import json
import requests
import cherrypy
import traceback
import voluptuous as v

import gear

from zuul.connection import BaseConnection
from zuul.lib.logutil import get_annotated_logger
from zuul.web.handler import BaseWebController
from zuul.lib.config import get_default
from zuul.model import Ref, Branch, Tag
from zuul.lib import dependson

from zuul.driver.pagure.paguremodel import PagureTriggerEvent, PullRequest

# Minimal Pagure version supported 5.3.0
#
# Pagure is similar to Github as it handles PullRequest where PR is a branch
# composed of one or more commits. A PR can be commented, evaluated, updated,
# CI flagged, and merged. A PR can be flagged (success/failure/pending) and
# this driver uses that capability.
#
# PR approval can be driven by (evaluation). This is done via comments that
# contains a :thumbsup: or :thumbsdown:. Pagure computes a score based on
# that and allows or not the merge of PR if the "minimal score to merge" is
# set in repository settings.
#
# PR approval can be also driven via PR metadata flag.
#
# This driver expects to receive repository events via webhooks and
# do event validation based on the source IP address of the event.
#
# The driver connection needs an user's API token with
# - "Merge a pull-request"
# - "Flag a pull-request"
# - "Comment on a pull-request"
#
# On each project to be integrated with Zuul needs:
#
# The web hook target must be (in repository settings):
# - http://<zuul-web>/zuul/api/connection/<conn-name>/payload
#
# Repository settings (to be checked):
# - Minimum score to merge pull-request = 0 or -1
# - Pull requests
# - Open metadata access to all (unchecked if approval)
#
# To define the connection in /etc/zuul/zuul.conf:
# [connection pagure.io]
# driver=pagure
# server=pagure.io
# baseurl=https://pagure.io
# api_token=QX29SXAW96C2CTLUNA5JKEEU65INGWTO2B5NHBDBRMF67S7PYZWCS0L1AKHXXXXX
# source_whitelist=8.43.85.75
#
# Current Non blocking issues:
# - Pagure does not reset the score when a PR code is updated
#   https://pagure.io/pagure/issue/3985
# - CI status flag updated field unit is second, better to have millisecond
#   unit to avoid unpossible sorting to get last status if two status set the
#   same second.
#   https://pagure.io/pagure/issue/4402
# - Zuul needs to be able to search commits that set a dependency (depends-on)
#   to a specific commit to reset jobs run when a dependency is changed. On
#   Gerrit and Github search through commits message is possible and used by
#   Zuul. Pagure does not offer this capability.

# Side notes
# - Idea would be to prevent PR merge by anybody else than Zuul.
# Pagure project option: "Activate Only assignee can merge pull-request"
# https://docs.pagure.org/pagure/usage/project_settings.html?highlight=score#activate-only-assignee-can-merge-pull-request


def _sign_request(body, secret):
    signature = hmac.new(
        secret.encode('utf-8'), body, hashlib.sha1).hexdigest()
    return signature, body


class PagureGearmanWorker(object):
    """A thread that answers gearman requests"""
    log = logging.getLogger("zuul.PagureGearmanWorker")

    def __init__(self, connection):
        self.config = connection.sched.config
        self.connection = connection
        self.thread = threading.Thread(target=self._run,
                                       name='pagure-gearman-worker')
        self._running = False
        handler = "pagure:%s:payload" % self.connection.connection_name
        self.jobs = {
            handler: self.handle_payload,
        }

    def _run(self):
        while self._running:
            try:
                job = self.gearman.getJob()
                try:
                    if job.name not in self.jobs:
                        self.log.exception("Exception while running job")
                        job.sendWorkException(
                            traceback.format_exc().encode('utf8'))
                        continue
                    output = self.jobs[job.name](json.loads(job.arguments))
                    job.sendWorkComplete(json.dumps(output))
                except Exception:
                    self.log.exception("Exception while running job")
                    job.sendWorkException(
                        traceback.format_exc().encode('utf8'))
            except gear.InterruptedError:
                pass
            except Exception:
                self.log.exception("Exception while getting job")

    def handle_payload(self, args):
        payload = args["payload"]

        self.log.info(
            "Pagure Webhook Received (id: %(msg_id)s, topic: %(topic)s)" % (
                payload))

        try:
            self.__dispatch_event(payload)
            output = {'return_code': 200}
        except Exception:
            output = {'return_code': 503}
            self.log.exception("Exception handling Pagure event:")

        return output

    def __dispatch_event(self, payload):
        event = payload['topic']
        try:
            self.log.info("Dispatching event %s" % event)
            self.connection.addEvent(payload, event)
        except Exception as err:
            message = 'Exception dispatching event: %s' % str(err)
            self.log.exception(message)
            raise Exception(message)

    def start(self):
        self._running = True
        server = self.config.get('gearman', 'server')
        port = get_default(self.config, 'gearman', 'port', 4730)
        ssl_key = get_default(self.config, 'gearman', 'ssl_key')
        ssl_cert = get_default(self.config, 'gearman', 'ssl_cert')
        ssl_ca = get_default(self.config, 'gearman', 'ssl_ca')
        self.gearman = gear.TextWorker('Zuul Pagure Connector')
        self.log.debug("Connect to gearman")
        self.gearman.addServer(server, port, ssl_key, ssl_cert, ssl_ca)
        self.log.debug("Waiting for server")
        self.gearman.waitForServer()
        self.log.debug("Registering")
        for job in self.jobs:
            self.gearman.registerFunction(job)
        self.thread.start()

    def stop(self):
        self._running = False
        self.gearman.stopWaitingForJobs()
        # We join here to avoid whitelisting the thread -- if it takes more
        # than 5s to stop in tests, there's a problem.
        self.thread.join(timeout=5)
        self.gearman.shutdown()


class PagureEventConnector(threading.Thread):
    """Move events from Pagure into the scheduler"""

    log = logging.getLogger("zuul.PagureEventConnector")

    def __init__(self, connection):
        super(PagureEventConnector, self).__init__()
        self.daemon = True
        self.connection = connection
        self._stopped = False
        self.metadata_notif = re.compile(
            r"^\*\*Metadata Update", re.MULTILINE)
        self.event_handler_mapping = {
            'pull-request.comment.added': self._event_issue_comment,
            'pull-request.closed': self._event_pull_request_closed,
            'pull-request.new': self._event_pull_request,
            'pull-request.flag.added': self._event_flag_added,
            'pull-request.flag.updated': self._event_flag_added,
            'git.receive': self._event_ref_updated,
            'git.branch.creation': self._event_ref_created,
            'git.branch.deletion': self._event_ref_deleted,
            'pull-request.initial_comment.edited':
                self._event_issue_initial_comment,
            'pull-request.tag.added':
                self._event_pull_request_tags_changed,
            'git.tag.creation': self._event_tag_created,
        }

    def stop(self):
        self._stopped = True
        self.connection.addEvent(None)

    def _handleEvent(self):
        ts, json_body, event_type = self.connection.getEvent()
        if self._stopped:
            return

        self.log.info("Received event: %s" % str(event_type))
        # self.log.debug("Event payload: %s " % json_body)

        if event_type not in self.event_handler_mapping:
            message = "Unhandled X-Pagure-Event: %s" % event_type
            self.log.info(message)
            return

        if event_type in self.event_handler_mapping:
            self.log.debug("Handling event: %s" % event_type)

        try:
            event = self.event_handler_mapping[event_type](json_body)
        except Exception:
            self.log.exception(
                'Exception when handling event: %s' % event_type)
            event = None

        if event:
            event.timestamp = ts
            if event.change_number:
                project = self.connection.source.getProject(event.project_name)
                self.connection._getChange(project,
                                           event.change_number,
                                           event.patch_number,
                                           refresh=True,
                                           url=event.change_url,
                                           event=event)
            event.project_hostname = self.connection.canonical_hostname
            self.connection.logEvent(event)
            self.connection.sched.addEvent(event)

    def _event_base(self, body, pull_data_field='pullrequest'):
        event = PagureTriggerEvent()

        if pull_data_field in body['msg']:
            data = body['msg'][pull_data_field]
            data['tags'] = body['msg'].get('tags', [])
            data['flag'] = body['msg'].get('flag')
            event.title = data.get('title')
            event.project_name = data.get('project', {}).get('fullname')
            event.change_number = data.get('id')
            event.updated_at = data.get('date_created')
            event.branch = data.get('branch')
            event.tags = data.get('tags', [])
            event.change_url = self.connection.getPullUrl(event.project_name,
                                                          event.change_number)
            event.ref = "refs/pull/%s/head" % event.change_number
            # commit_stop is the tip of the PR branch
            event.patch_number = data.get('commit_stop')
            event.type = 'pg_pull_request'
        else:
            data = body['msg']
            event.type = 'pg_push'
        return event, data

    def _event_issue_initial_comment(self, body):
        """ Handles pull request initial comment change """
        event, _ = self._event_base(body)
        event.action = 'changed'
        return event

    def _event_pull_request_tags_changed(self, body):
        """ Handles pull request metadata change """
        # pull-request.tag.added/removed use pull_request in payload body
        event, _ = self._event_base(body, pull_data_field='pull_request')
        event.action = 'tagged'
        return event

    def _event_issue_comment(self, body):
        """ Handles pull request comments """
        # https://fedora-fedmsg.readthedocs.io/en/latest/topics.html#pagure-pull-request-comment-added
        event, data = self._event_base(body)
        last_comment = data.get('comments', [])[-1]
        if (last_comment.get('notification') is True and
                not self.metadata_notif.match(
                    last_comment.get('comment', ''))):
            # An updated PR (new commits) triggers the comment.added
            # event. A message is added by pagure on the PR but notification
            # is set to true.
            event.action = 'changed'
        else:
            if last_comment.get('comment', '').find(':thumbsup:') >= 0:
                event.action = 'thumbsup'
                event.type = 'pg_pull_request_review'
            elif last_comment.get('comment', '').find(':thumbsdown:') >= 0:
                event.action = 'thumbsdown'
                event.type = 'pg_pull_request_review'
            else:
                event.action = 'comment'
        # Assume last comment is the one that have triggered the event
        event.comment = last_comment.get('comment')
        return event

    def _event_pull_request(self, body):
        """ Handles pull request opened event """
        # https://fedora-fedmsg.readthedocs.io/en/latest/topics.html#pagure-pull-request-new
        event, data = self._event_base(body)
        event.action = 'opened'
        return event

    def _event_pull_request_closed(self, body):
        """ Handles pull request closed event """
        event, data = self._event_base(body)
        event.action = 'closed'
        return event

    def _event_flag_added(self, body):
        """ Handles flag added event """
        # https://fedora-fedmsg.readthedocs.io/en/latest/topics.html#pagure-pull-request-flag-added
        event, data = self._event_base(body)
        event.status = data['flag']['status']
        event.action = 'status'
        return event

    def _event_tag_created(self, body):
        event, data = self._event_base(body)
        event.project_name = data.get('project_fullname')
        event.tag = data.get('tag')
        event.ref = 'refs/tags/%s' % event.tag
        event.oldrev = None
        event.newrev = data.get('rev')
        return event

    def _event_ref_updated(self, body):
        """ Handles ref updated """
        # https://fedora-fedmsg.readthedocs.io/en/latest/topics.html#pagure-git-receive
        event, data = self._event_base(body)
        event.project_name = data.get('project_fullname')
        event.branch = data.get('branch')
        event.ref = 'refs/heads/%s' % event.branch
        event.newrev = data.get('end_commit')
        event.oldrev = data.get('old_commit')
        event.branch_updated = True
        return event

    def _event_ref_created(self, body):
        """ Handles ref created """
        event, data = self._event_base(body)
        event.project_name = data.get('project_fullname')
        event.branch = data.get('branch')
        event.ref = 'refs/heads/%s' % event.branch
        event.newrev = data.get('rev')
        event.oldrev = '0' * 40
        event.branch_created = True
        self.connection.project_branch_cache[
            event.project_name].append(event.branch)
        return event

    def _event_ref_deleted(self, body):
        """ Handles ref deleted """
        event, data = self._event_base(body)
        event.project_name = data.get('project_fullname')
        event.branch = data.get('branch')
        event.ref = 'refs/heads/%s' % event.branch
        event.oldrev = data.get('rev')
        event.newrev = '0' * 40
        event.branch_deleted = True
        self.connection.project_branch_cache[
            event.project_name].remove(event.branch)
        return event

    def run(self):
        while True:
            if self._stopped:
                return
            try:
                self._handleEvent()
            except Exception:
                self.log.exception("Exception moving Pagure event:")
            finally:
                self.connection.eventDone()


class PagureAPIClientException(Exception):
    pass


class PagureAPIClient():
    log = logging.getLogger("zuul.PagureAPIClient")

    def __init__(
            self, baseurl, api_token, project):
        self.session = requests.Session()
        self.base_url = '%s/api/0/' % baseurl
        self.api_token = api_token
        self.project = project
        self.headers = {'Authorization': 'token %s' % self.api_token}

    def _manage_error(self, data, code, url, verb):
        if code < 400:
            return
        else:
            raise PagureAPIClientException(
                "Unable to %s on %s (code: %s) due to: %s" % (
                    verb, url, code, data
                ))

    def get(self, url):
        self.log.debug("Getting resource %s ..." % url)
        ret = self.session.get(url, headers=self.headers)
        self.log.debug("GET returned (code: %s): %s" % (
            ret.status_code, ret.text))
        return ret.json(), ret.status_code, ret.url, 'GET'

    def post(self, url, params=None):
        self.log.info(
            "Posting on resource %s, params (%s) ..." % (url, params))
        ret = self.session.post(url, data=params, headers=self.headers)
        self.log.debug("POST returned (code: %s): %s" % (
            ret.status_code, ret.text))
        return ret.json(), ret.status_code, ret.url, 'POST'

    def whoami(self):
        path = '-/whoami'
        resp = self.post(self.base_url + path)
        self._manage_error(*resp)
        return resp[0]['username']

    def get_project_branches(self):
        path = '%s/git/branches' % self.project
        resp = self.get(self.base_url + path)
        self._manage_error(*resp)
        return resp[0].get('branches', [])

    def get_pr(self, number):
        path = '%s/pull-request/%s' % (self.project, number)
        resp = self.get(self.base_url + path)
        self._manage_error(*resp)
        return resp[0]

    def get_pr_diffstats(self, number):
        path = '%s/pull-request/%s/diffstats' % (self.project, number)
        resp = self.get(self.base_url + path)
        self._manage_error(*resp)
        return resp[0]

    def get_pr_flags(self, number, owner, last=False):
        path = '%s/pull-request/%s/flag' % (self.project, number)
        resp = self.get(self.base_url + path)
        self._manage_error(*resp)
        data = resp[0]
        owned_flags = [
            flag for flag in data['flags']
            if flag['user']['name'] == owner]
        if last:
            if owned_flags:
                return owned_flags[0]
            else:
                return {}
        else:
            return owned_flags

    def set_pr_flag(
            self, number, status, url, description, app_name, username):
        flag_uid = "%s-%s-%s" % (username, number, self.project)
        params = {
            "username": app_name,
            "comment": "Jobs result is %s" % status,
            "uid": flag_uid[:32],
            "status": status,
            "url": url}
        path = '%s/pull-request/%s/flag' % (self.project, number)
        resp = self.post(self.base_url + path, params)
        self._manage_error(*resp)
        return resp[0]

    def comment_pull(self, number, message):
        params = {"comment": message}
        path = '%s/pull-request/%s/comment' % (self.project, number)
        resp = self.post(self.base_url + path, params)
        self._manage_error(*resp)
        return resp[0]

    def merge_pr(self, number):
        path = '%s/pull-request/%s/merge' % (self.project, number)
        resp = self.post(self.base_url + path)
        self._manage_error(*resp)
        return resp[0]

    def get_webhook_token(self):
        """ A project collaborator's api token must be used with that endpoint
        """
        path = '%s/webhook/token' % self.project
        resp = self.get(self.base_url + path)
        self._manage_error(*resp)
        return resp[0]['webhook']['token']


class PagureConnection(BaseConnection):
    driver_name = 'pagure'
    log = logging.getLogger("zuul.PagureConnection")

    def __init__(self, driver, connection_name, connection_config):
        super(PagureConnection, self).__init__(
            driver, connection_name, connection_config)
        self._change_cache = {}
        self.project_branch_cache = {}
        self.projects = {}
        self.server = self.connection_config.get('server', 'pagure.io')
        self.canonical_hostname = self.connection_config.get(
            'canonical_hostname', self.server)
        self.git_ssh_key = self.connection_config.get('sshkey')
        self.api_token = self.connection_config.get('api_token')
        self.app_name = self.connection_config.get(
            'app_name', 'Zuul')
        self.username = None
        self.baseurl = self.connection_config.get(
            'baseurl', 'https://%s' % self.server).rstrip('/')
        self.cloneurl = self.connection_config.get(
            'cloneurl', self.baseurl).rstrip('/')
        self.source_whitelist = self.connection_config.get(
            'source_whitelist', '').split(',')
        self.webhook_tokens = {}
        self.source = driver.getSource(self)
        self.event_queue = queue.Queue()
        self.metadata_notif = re.compile(
            r"^\*\*Metadata Update", re.MULTILINE)
        self.sched = None

    def onLoad(self):
        self.log.info('Starting Pagure connection: %s' % self.connection_name)
        self.gearman_worker = PagureGearmanWorker(self)
        self.log.info('Starting event connector')
        self._start_event_connector()
        self.log.info('Starting GearmanWorker')
        self.gearman_worker.start()

    def _start_event_connector(self):
        self.pagure_event_connector = PagureEventConnector(self)
        self.pagure_event_connector.start()

    def _stop_event_connector(self):
        if self.pagure_event_connector:
            self.pagure_event_connector.stop()
            self.pagure_event_connector.join()

    def onStop(self):
        if hasattr(self, 'gearman_worker'):
            self.gearman_worker.stop()
            self._stop_event_connector()

    def addEvent(self, data, event=None):
        return self.event_queue.put((time.time(), data, event))

    def getEvent(self):
        return self.event_queue.get()

    def eventDone(self):
        self.event_queue.task_done()

    def set_my_username(self, client):
        self.log.debug("Fetching my username ...")
        self.username = client.whoami()
        self.log.debug("My username is %s" % self.username)

    def get_project_api_client(self, project):
        self.log.debug("Building project %s api_client" % project)
        client = PagureAPIClient(self.baseurl, self.api_token, project)
        if not self.username:
            self.set_my_username(client)
        return client

    def get_project_webhook_token(self, project, force_refresh=False):
        token = self.webhook_tokens.get(project)
        if token and not force_refresh:
            self.log.debug(
                "Fetching project %s webhook token from cache" % project)
            return token
        else:
            pagure = self.get_project_api_client(project)
            token = pagure.get_webhook_token()
            self.webhook_tokens[project] = token
            self.log.debug(
                "Fetching project %s webhook token from API" % project)
            return token

    def maintainCache(self, relevant):
        remove = set()
        for key, change in self._change_cache.items():
            if change not in relevant:
                remove.add(key)
        for key in remove:
            del self._change_cache[key]

    def clearCache(self):
        self.project_branch_cache = {}

    def getWebController(self, zuul_web):
        return PagureWebController(zuul_web, self)

    def validateWebConfig(self, config, connections):
        return True

    def getProject(self, name):
        return self.projects.get(name)

    def addProject(self, project):
        self.projects[project.name] = project

    def getPullUrl(self, project, number):
        return '%s/pull-request/%s' % (self.getGitwebUrl(project), number)

    def getGitwebUrl(self, project, sha=None):
        url = '%s/%s' % (self.baseurl, project)
        if sha is not None:
            url += '/c/%s' % sha
        return url

    def getProjectBranches(self, project, tenant):
        branches = self.project_branch_cache.get(project.name)

        if branches is not None:
            return branches

        pagure = self.get_project_api_client(project.name)
        branches = pagure.get_project_branches()
        self.project_branch_cache[project.name] = branches

        self.log.info("Got branches for %s" % project.name)
        return branches

    def getGitUrl(self, project):
        return '%s/%s' % (self.cloneurl, project.name)

    def getChange(self, event, refresh=False):
        project = self.source.getProject(event.project_name)
        if event.change_number:
            self.log.info("Getting change for %s#%s" % (
                project, event.change_number))
            change = self._getChange(
                project, event.change_number, event.patch_number,
                refresh=refresh, event=event)
            change.is_current_patchset = (change.pr.get('commit_stop') ==
                                          event.patch_number)
        else:
            self.log.info("Getting change for %s ref:%s" % (
                project, event.ref))
            if event.ref and event.ref.startswith('refs/tags/'):
                change = Tag(project)
                change.tag = event.tag
                change.branch = None
            elif event.ref and event.ref.startswith('refs/heads/'):
                change = Branch(project)
                change.branch = event.branch
            else:
                change = Ref(project)
                change.branch = None
            change.ref = event.ref
            change.oldrev = event.oldrev
            change.newrev = event.newrev
            change.url = self.getGitwebUrl(project, sha=event.newrev)

            # Pagure does not send files details in the git-receive event.
            # Explicitly set files to None and let the pipelines processor
            # call the merger asynchronuously
            change.files = None

        return change

    def _getChange(self, project, number, patchset=None,
                   refresh=False, url=None, event=None):
        key = (project.name, number, patchset)
        change = self._change_cache.get(key)
        if change and not refresh:
            self.log.debug("Getting change from cache %s" % str(key))
            return change
        if not change:
            change = PullRequest(project.name)
            change.project = project
            change.number = number
            # patchset is the tips commit of the PR
            change.patchset = patchset
            change.url = url
            change.uris = [
                '%s/%s/pull/%s' % (self.baseurl, project, number),
            ]
        self._change_cache[key] = change
        try:
            self.log.debug("Getting change pr#%s from project %s" % (
                number, project.name))
            self._updateChange(change, event)
        except Exception:
            if key in self._change_cache:
                del self._change_cache[key]
            raise
        return change

    def _hasRequiredStatusChecks(self, change):
        pagure = self.get_project_api_client(change.project.name)
        flag = pagure.get_pr_flags(change.number, self.username, last=True)
        return True if flag.get('status', '') == 'success' else False

    def canMerge(self, change, allow_needs, event=None):
        log = get_annotated_logger(self.log, event)
        pagure = self.get_project_api_client(change.project.name)
        pr = pagure.get_pr(change.number)

        mergeable = False
        if pr.get('cached_merge_status') in ('FFORWARD', 'MERGE'):
            mergeable = True

        ci_flag = False
        if self._hasRequiredStatusChecks(change):
            ci_flag = True

        # By default project get -1 in "Minimum score to merge pull-request"
        # But this makes the API to return None for threshold_reached. We need
        # to handle this case as threshold_reached: True because it means
        # no minimal score configured.
        threshold = pr.get('threshold_reached')
        if threshold is None:
            threshold = True

        log.debug(
            'PR %s#%s mergeability details mergeable: %s '
            'flag: %s threshold: %s', change.project.name, change.number,
            mergeable, ci_flag, threshold)

        can_merge = mergeable and ci_flag and threshold

        log.info('Check PR %s#%s mergeability can_merge: %s',
                 change.project.name, change.number, can_merge)
        return can_merge

    def getPull(self, project_name, number, event=None):
        log = get_annotated_logger(self.log, event=event)
        pagure = self.get_project_api_client(project_name)
        pr = pagure.get_pr(number)
        diffstats = pagure.get_pr_diffstats(number)
        pr['files'] = list(diffstats.keys())
        log.info('Got PR %s#%s', project_name, number)
        return pr

    def getStatus(self, project, number):
        return self.getCommitStatus(project.name, number)

    def getScore(self, pr):
        score_board = {}
        last_pr_code_updated = 0
        # First get last PR updated date
        for comment in pr.get('comments', []):
            # PR updated are reported as comment but with the notification flag
            if comment['notification']:
                # Ignore metadata update such as assignee and tags
                if self.metadata_notif.match(comment.get('comment', '')):
                    continue
                date = int(comment['date_created'])
                if date > last_pr_code_updated:
                    last_pr_code_updated = date
        # Now compute the score
        # TODO(fbo): Pagure does not reset the score when a PR code is updated
        # This code block computes the score based on votes after the last PR
        # update. This should be proposed upstream
        # https://pagure.io/pagure/issue/3985
        for comment in pr.get('comments', []):
            author = comment['user']['fullname']
            date = int(comment['date_created'])
            # Only handle score since the last PR update
            if date >= last_pr_code_updated:
                score_board.setdefault(author, 0)
                # Use the same strategy to compute the score than Pagure
                if comment.get('comment', '').find(':thumbsup:') >= 0:
                    score_board[author] += 1
                if comment.get('comment', '').find(':thumbsdown:') >= 0:
                    score_board[author] -= 1
        return sum(score_board.values())

    def _updateChange(self, change, event):
        self.log.info("Updating change from pagure %s" % change)
        change.pr = self.getPull(change.project.name, change.number)
        change.ref = "refs/pull/%s/head" % change.number
        change.branch = change.pr.get('branch')
        change.patchset = change.pr.get('commit_stop')
        change.files = change.pr.get('files')
        change.title = change.pr.get('title')
        change.tags = change.pr.get('tags')
        change.open = change.pr.get('status') == 'Open'
        change.is_merged = change.pr.get('status') == 'Merged'
        change.status = self.getStatus(change.project, change.number)
        change.score = self.getScore(change.pr)
        change.message = change.pr.get('initial_comment') or ''
        # last_updated seems to be touch for comment changed/flags - that's OK
        change.updated_at = change.pr.get('last_updated')
        self.log.info("Updated change from pagure %s" % change)

        if self.sched:
            self.sched.onChangeUpdated(change, event)

        return change

    def commentPull(self, project, number, message):
        pagure = self.get_project_api_client(project)
        pagure.comment_pull(number, message)
        self.log.info("Commented on PR %s#%s", project, number)

    def setCommitStatus(self, project, number, state, url='',
                        description='', context=''):
        pagure = self.get_project_api_client(project)
        pagure.set_pr_flag(
            number, state, url, description, self.app_name, self.username)
        self.log.info("Set pull-request CI flag status : %s" % description)
        # Wait for 1 second as flag timestamp is by second
        time.sleep(1)

    def getCommitStatus(self, project, number):
        pagure = self.get_project_api_client(project)
        flag = pagure.get_pr_flags(number, self.username, last=True)
        self.log.info(
            "Got pull-request CI status for PR %s on %s status: %s" % (
                number, project, flag.get('status')))
        return flag.get('status')

    def getChangesDependingOn(self, change, projects, tenant):
        """ Reverse lookup of PR depending on this one
        """
        # TODO(fbo) No way to Query pagure to search accross projects' PRs for
        # a the depends-on string in PR initial message. Not a blocker
        # for now, let's workaround using the local change cache !
        changes_dependencies = []
        for cached_change_id, _change in self._change_cache.items():
            for dep_header in dependson.find_dependency_headers(
                    _change.message):
                if change.url in dep_header:
                    changes_dependencies.append(_change)
        return changes_dependencies

    def mergePull(self, project, number):
        pagure = self.get_project_api_client(project)
        pagure.merge_pr(number)
        self.log.debug("Merged PR %s#%s", project, number)


class PagureWebController(BaseWebController):

    log = logging.getLogger("zuul.PagureWebController")

    def __init__(self, zuul_web, connection):
        self.connection = connection
        self.zuul_web = zuul_web

    def _source_whitelisted(self, remote_ip, forwarded_ip):
        if remote_ip and remote_ip in self.connection.source_whitelist:
            return True
        if forwarded_ip and forwarded_ip in self.connection.source_whitelist:
            return True

    def _validate(self, body, token, request_signature):
        signature, payload = _sign_request(body, token)
        if not hmac.compare_digest(str(signature), str(request_signature)):
            self.log.info(
                "Missmatch (Payload Signature: %s, Request Signature: %s)" % (
                    signature, request_signature))
            return False
        return True

    def _validate_signature(self, body, headers):
        try:
            request_signature = headers['x-pagure-signature']
        except KeyError:
            raise cherrypy.HTTPError(
                401, 'x-pagure-signature header missing.')

        project = headers['x-pagure-project']
        token = self.connection.get_project_webhook_token(project)
        if not self._validate(body, token, request_signature):
            # Give a second attempt as a token could have been
            # re-generated server side. Refresh the token then retry.
            self.log.info(
                "Refresh cached webhook token and re-check signature")
            token = self.connection.get_project_webhook_token(
                project, force_refresh=True)
            if not self._validate(body, token, request_signature):
                raise cherrypy.HTTPError(
                    401,
                    'Request signature does not match calculated payload '
                    'signature. Check that secret is correct.')

    @cherrypy.expose
    @cherrypy.tools.json_out(content_type='application/json; charset=utf-8')
    def payload(self):
        # https://docs.pagure.org/pagure/usage/using_webhooks.html
        headers = dict()
        for key, value in cherrypy.request.headers.items():
            headers[key.lower()] = value
        body = cherrypy.request.body.read()
        if not self._source_whitelisted(
                getattr(cherrypy.request.remote, 'ip'),
                headers.get('x-forwarded-for')):
            self._validate_signature(body, headers)
        else:
            self.log.info(
                "Payload origin IP address whitelisted. Skip verify")

        json_payload = json.loads(body.decode('utf-8'))
        job = self.zuul_web.rpc.submitJob(
            'pagure:%s:payload' % self.connection.connection_name,
            {'payload': json_payload})

        return json.loads(job.data[0])


def getSchema():
    pagure_connection = v.Any(str, v.Schema(dict))
    return pagure_connection
