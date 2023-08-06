# Copyright 2019 Red Hat, Inc.
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
import threading
import json
import queue
import cherrypy
import voluptuous as v
import time
import uuid
import requests

import dateutil.parser

from urllib.parse import quote_plus
from typing import List, Optional

from zuul.connection import CachedBranchConnection
from zuul.web.handler import BaseWebController
from zuul.lib.gearworker import ZuulGearWorker
from zuul.lib.logutil import get_annotated_logger
from zuul.model import Branch, Project, Ref, Tag

from zuul.driver.gitlab.gitlabmodel import GitlabTriggerEvent, MergeRequest


class GitlabGearmanWorker(object):
    """A thread that answers gearman requests"""
    log = logging.getLogger("zuul.GitlabGearmanWorker")

    def __init__(self, connection):
        self.config = connection.sched.config
        self.connection = connection
        handler = "gitlab:%s:payload" % self.connection.connection_name
        self.jobs = {
            handler: self.handle_payload,
        }
        self.gearworker = ZuulGearWorker(
            'Zuul Gitlab Worker',
            'zuul.GitlabGearmanWorker',
            'gitlab',
            self.config,
            self.jobs)

    def handle_payload(self, job):
        args = json.loads(job.arguments)
        payload = args["payload"]

        self.log.info(
            "Gitlab Webhook Received event kind: %(object_kind)s" % payload)

        try:
            self.__dispatch_event(payload)
            output = {'return_code': 200}
        except Exception:
            output = {'return_code': 503}
            self.log.exception("Exception handling Gitlab event:")

        job.sendWorkComplete(json.dumps(output))

    def __dispatch_event(self, payload):
        self.log.info(payload)
        event = payload['object_kind']
        try:
            self.log.info("Dispatching event %s" % event)
            self.connection.addEvent(payload, event)
        except Exception as err:
            message = 'Exception dispatching event: %s' % str(err)
            self.log.exception(message)
            raise Exception(message)

    def start(self):
        self.gearworker.start()

    def stop(self):
        self.gearworker.stop()


class GitlabEventConnector(threading.Thread):
    """Move events from Gitlab into the scheduler"""

    log = logging.getLogger("zuul.GitlabEventConnector")

    def __init__(self, connection):
        super(GitlabEventConnector, self).__init__()
        self.daemon = True
        self.connection = connection
        self._stopped = False
        self.event_handler_mapping = {
            'merge_request': self._event_merge_request,
            'note': self._event_note,
            'push': self._event_push,
            'tag_push': self._event_tag_push,
        }

    def stop(self):
        self._stopped = True
        self.connection.addEvent(None)

    def _event_base(self, body):
        event = GitlabTriggerEvent()
        attrs = body.get('object_attributes')
        if attrs:
            event.updated_at = int(dateutil.parser.parse(
                attrs['updated_at']).timestamp())
            event.created_at = int(dateutil.parser.parse(
                attrs['created_at']).timestamp())
        event.project_name = body['project']['path_with_namespace']
        return event

    # https://docs.gitlab.com/ee/user/project/integrations/webhooks.html#merge-request-events
    def _event_merge_request(self, body):
        event = self._event_base(body)
        attrs = body['object_attributes']
        event.title = attrs['title']
        event.change_number = attrs['iid']
        event.ref = "refs/merge-requests/%s/head" % event.change_number
        event.branch = attrs['target_branch']
        event.patch_number = attrs['last_commit']['id']
        event.change_url = self.connection.getMRUrl(event.project_name,
                                                    event.change_number)
        if attrs['action'] == 'open':
            event.action = 'opened'
        elif attrs['action'] == 'merge':
            event.action = 'merged'
        elif attrs['action'] == 'update' and "labels" not in body["changes"]:
            event.action = 'changed'
        elif attrs['action'] == 'update' and "labels" in body["changes"]:
            event.action = 'labeled'
            previous_labels = [
                label["title"] for
                label in body["changes"]["labels"]["previous"]]
            current_labels = [
                label["title"] for
                label in body["changes"]["labels"]["current"]]
            new_labels = set(current_labels) - set(previous_labels)
            event.labels = new_labels
        elif attrs['action'] in ('approved', 'unapproved'):
            event.action = attrs['action']
        else:
            # Do not handle other merge_request action for now.
            return None
        event.type = 'gl_merge_request'
        return event

    # https://docs.gitlab.com/ee/user/project/integrations/webhooks.html#comment-on-merge-request
    def _event_note(self, body):
        event = self._event_base(body)
        event.comment = body['object_attributes']['note']
        mr = body['merge_request']
        event.title = mr['title']
        event.change_number = mr['iid']
        # mr['last_commit']['id'] is the commit SHA
        event.patch_number = mr['last_commit']['id']
        event.ref = "refs/merge-requests/%s/head" % event.change_number
        event.branch = mr['target_branch']
        event.change_url = self.connection.getMRUrl(event.project_name,
                                                    event.change_number)
        event.action = 'comment'
        event.type = 'gl_merge_request'
        return event

    # https://docs.gitlab.com/ee/user/project/integrations/webhooks.html#push-events
    def _event_push(self, body):
        event = self._event_base(body)
        event.branch = body['ref'].replace('refs/heads/', '')
        event.ref = body['ref']
        event.newrev = body['after']
        event.oldrev = body['before']
        event.type = 'gl_push'

        self.connection.clearConnectionCacheOnBranchEvent(event)

        return event

    # https://gitlab.com/help/user/project/integrations/webhooks#tag-events
    def _event_tag_push(self, body):
        event = self._event_base(body)
        event.ref = body['ref']
        event.newrev = body['after']
        event.oldrev = None
        event.tag = body['ref'].replace('refs/tags/', '')
        event.type = 'gl_push'
        return event

    def _handleEvent(self):
        ts, json_body, event_type = self.connection.getEvent()
        if self._stopped:
            return

        self.log.info("Received event: %s" % str(event_type))

        if event_type not in self.event_handler_mapping:
            message = "Unhandled Gitlab event: %s" % event_type
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
            event.zuul_event_id = str(uuid.uuid4())
            event.timestamp = ts
            event.project_hostname = self.connection.canonical_hostname
            if event.change_number:
                project = self.connection.source.getProject(event.project_name)
                self.connection._getChange(project,
                                           event.change_number,
                                           event.patch_number,
                                           refresh=True,
                                           url=event.change_url,
                                           event=event)

            # If this event references a branch and we're excluding
            # unprotected branches, we might need to check whether the
            # branch is now protected.
            if hasattr(event, "branch") and event.branch:
                self.connection.checkBranchCache(event.project_name, event)

            self.connection.logEvent(event)
            self.connection.sched.addEvent(event)

    def run(self):
        while True:
            if self._stopped:
                return
            try:
                self._handleEvent()
            except Exception:
                self.log.exception("Exception moving Gitlab event:")
            finally:
                self.connection.eventDone()


class GitlabAPIClientException(Exception):
    pass


class GitlabAPIClient():
    log = logging.getLogger("zuul.GitlabAPIClient")

    def __init__(self, baseurl, api_token):
        self.session = requests.Session()
        self.baseurl = '%s/api/v4/' % baseurl
        self.api_token = api_token
        self.headers = {'Authorization': 'Bearer %s' % (
            self.api_token)}

    def _manage_error(self, data, code, url, verb, zuul_event_id=None):
        if code < 400:
            return
        else:
            raise GitlabAPIClientException(
                "[e: %s] Unable to %s on %s (code: %s) due to: %s" % (
                    zuul_event_id, verb, url, code, data
                ))

    def get(self, url, zuul_event_id=None):
        log = get_annotated_logger(self.log, zuul_event_id)
        log.debug("Getting resource %s ..." % url)
        ret = self.session.get(url, headers=self.headers)
        log.debug("GET returned (code: %s): %s" % (
            ret.status_code, ret.text))
        return ret.json(), ret.status_code, ret.url, 'GET'

    def post(self, url, params=None, zuul_event_id=None):
        log = get_annotated_logger(self.log, zuul_event_id)
        log.info(
            "Posting on resource %s, params (%s) ..." % (url, params))
        ret = self.session.post(url, data=params, headers=self.headers)
        log.debug("POST returned (code: %s): %s" % (
            ret.status_code, ret.text))
        return ret.json(), ret.status_code, ret.url, 'POST'

    def put(self, url, params=None, zuul_event_id=None):
        log = get_annotated_logger(self.log, zuul_event_id)
        log.info(
            "Put on resource %s, params (%s) ..." % (url, params))
        ret = self.session.put(url, data=params, headers=self.headers)
        log.debug("PUT returned (code: %s): %s" % (
            ret.status_code, ret.text))
        return ret.json(), ret.status_code, ret.url, 'PUT'

    # https://docs.gitlab.com/ee/api/merge_requests.html#get-single-mr
    def get_mr(self, project_name, number, zuul_event_id=None):
        path = "/projects/%s/merge_requests/%s" % (
            quote_plus(project_name), number)
        resp = self.get(self.baseurl + path, zuul_event_id=zuul_event_id)
        self._manage_error(*resp, zuul_event_id=zuul_event_id)
        return resp[0]

    # https://docs.gitlab.com/ee/api/branches.html#list-repository-branches
    def get_project_branches(self, project_name, exclude_unprotected,
                             zuul_event_id=None):
        if exclude_unprotected:
            path = "/projects/{}/protected_branches"
        else:
            path = "/projects/{}/repository/branches"
        url = self.baseurl + path.format(quote_plus(project_name))
        resp = self.get(url, zuul_event_id=zuul_event_id)
        self._manage_error(*resp, zuul_event_id=zuul_event_id)
        return [branch['name'] for branch in resp[0]]

    # https://docs.gitlab.com/ee/api/branches.html#get-single-repository-branch
    def get_project_branch(self, project_name, branch_name,
                           zuul_event_id=None):
        path = "/projects/{}/repository/branches/{}"
        path = path.format(quote_plus(project_name), quote_plus(branch_name))
        url = self.baseurl + path
        resp = self.get(url, zuul_event_id=zuul_event_id)
        try:
            self._manage_error(*resp, zuul_event_id=zuul_event_id)
        except GitlabAPIClientException:
            if resp[1] != 404:
                raise
            return {}
        return resp[0]

    # https://docs.gitlab.com/ee/api/notes.html#create-new-merge-request-note
    def comment_mr(self, project_name, number, msg, zuul_event_id=None):
        path = "/projects/%s/merge_requests/%s/notes" % (
            quote_plus(project_name), number)
        params = {'body': msg}
        resp = self.post(
            self.baseurl + path, params=params,
            zuul_event_id=zuul_event_id)
        self._manage_error(*resp, zuul_event_id=zuul_event_id)
        return resp[0]

    # https://docs.gitlab.com/ee/api/merge_request_approvals.html#approve-merge-request
    def approve_mr(self, project_name, number, patchset, approve=True,
                   zuul_event_id=None):
        approve = 'approve' if approve else 'unapprove'
        path = "/projects/%s/merge_requests/%s/%s" % (
            quote_plus(project_name), number, approve)
        params = {'sha': patchset} if approve else {}
        resp = self.post(
            self.baseurl + path, params=params,
            zuul_event_id=zuul_event_id)
        try:
            self._manage_error(*resp, zuul_event_id=zuul_event_id)
        except GitlabAPIClientException:
            # approve and unapprove endpoint could return code 401 whether the
            # actual state of the Merge Request approval. Two call on approve
            # endpoint the second call return 401.
            # 409 is returned when current HEAD of the merge request doesn't
            # match the 'sha' parameter.
            if resp[1] not in (401, 409):
                raise
            elif approve == 'approve' and resp[1] == 409:
                log = get_annotated_logger(self.log, zuul_event_id)
                log.error('Fail to approve the merge request: %s' % resp[0])
                return
        return resp[0]

    # https://docs.gitlab.com/ee/api/merge_request_approvals.html#get-configuration-1
    def get_mr_approvals_status(self, project_name, number,
                                zuul_event_id=None):
        path = "/projects/%s/merge_requests/%s/approvals" % (
            quote_plus(project_name), number)
        resp = self.get(self.baseurl + path, zuul_event_id=zuul_event_id)
        self._manage_error(*resp, zuul_event_id=zuul_event_id)
        return resp[0]

    # https://docs.gitlab.com/ee/api/merge_requests.html#accept-mr
    def merge_mr(self, project_name, number,
                 zuul_event_id=None):
        path = "/projects/%s/merge_requests/%s/merge" % (
            quote_plus(project_name), number)
        resp = self.put(self.baseurl + path, zuul_event_id=zuul_event_id)
        self._manage_error(*resp, zuul_event_id=zuul_event_id)
        return resp[0]


class GitlabConnection(CachedBranchConnection):
    driver_name = 'gitlab'
    log = logging.getLogger("zuul.GitlabConnection")
    payload_path = 'payload'

    def __init__(self, driver, connection_name, connection_config):
        super(GitlabConnection, self).__init__(
            driver, connection_name, connection_config)
        self.projects = {}
        self._change_cache = {}
        self.server = self.connection_config.get('server', 'gitlab.com')
        self.baseurl = self.connection_config.get(
            'baseurl', 'https://%s' % self.server).rstrip('/')
        self.cloneurl = self.connection_config.get(
            'cloneurl', self.baseurl).rstrip('/')
        self.canonical_hostname = self.connection_config.get(
            'canonical_hostname', self.server)
        self.webhook_token = self.connection_config.get(
            'webhook_token', '')
        self.api_token = self.connection_config.get(
            'api_token', '')
        self.gl_client = GitlabAPIClient(self.baseurl, self.api_token)
        self.sched = None
        self.event_queue = queue.Queue()
        self.source = driver.getSource(self)

    def _start_event_connector(self):
        self.gitlab_event_connector = GitlabEventConnector(self)
        self.gitlab_event_connector.start()

    def _stop_event_connector(self):
        if self.gitlab_event_connector:
            self.gitlab_event_connector.stop()
            self.gitlab_event_connector.join()

    def onLoad(self):
        self.log.info('Starting Gitlab connection: %s' % self.connection_name)
        self.gearman_worker = GitlabGearmanWorker(self)
        self.log.info('Starting event connector')
        self._start_event_connector()
        self.log.info('Starting GearmanWorker')
        self.gearman_worker.start()

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

    def getWebController(self, zuul_web):
        return GitlabWebController(zuul_web, self)

    def getProject(self, name):
        return self.projects.get(name)

    def addProject(self, project):
        self.projects[project.name] = project

    def _fetchProjectBranches(self, project: Project,
                              exclude_unprotected: bool) -> List[str]:
        branches = self.gl_client.get_project_branches(project.name,
                                                       exclude_unprotected)
        return branches

    def isBranchProtected(self, project_name: str, branch_name: str,
                          zuul_event_id=None) -> Optional[bool]:
        branch = self.gl_client.get_project_branch(project_name, branch_name,
                                                   zuul_event_id)
        return branch.get('protected')

    def getGitwebUrl(self, project, sha=None):
        url = '%s/%s' % (self.baseurl, project)
        if sha is not None:
            url += '/tree/%s' % sha
        return url

    def getMRUrl(self, project, number):
        return '%s/%s/merge_requests/%s' % (self.baseurl, project, number)

    def getGitUrl(self, project):
        return '%s/%s.git' % (self.cloneurl, project.name)

    def getChange(self, event, refresh=False):
        project = self.source.getProject(event.project_name)
        if event.change_number:
            self.log.info("Getting change for %s#%s" % (
                project, event.change_number))
            change = self._getChange(
                project, event.change_number, event.patch_number,
                refresh=refresh, event=event)
            change.is_current_patchset = (change.patchset ==
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

            change.files = None
        return change

    def _getChange(self, project, number, patch_number=None,
                   refresh=False, url=None, event=None):
        log = get_annotated_logger(self.log, event)
        key = (project.name, str(number), str(patch_number))
        change = self._change_cache.get(key)
        if change and not refresh:
            log.debug("Getting change from cache %s" % str(key))
            return change
        if not change:
            change = MergeRequest(project.name)
            change.project = project
            change.number = number
            # patch_number is the tips commit SHA of the MR
            change.patchset = patch_number
            change.url = url or self.getMRUrl(project.name, number)
            change.uris = [change.url.split('://', 1)[-1]]  # remove scheme
        self._change_cache[key] = change
        try:
            log.debug("Getting change mr#%s from project %s" % (
                number, project.name))
            self._updateChange(change, event)
        except Exception:
            if key in self._change_cache:
                del self._change_cache[key]
            raise
        return change

    def _updateChange(self, change, event):
        log = get_annotated_logger(self.log, event)
        log.info("Updating change from Gitlab %s" % change)
        change.mr = self.getMR(
            change.project.name, change.number, event=event)
        change.ref = "refs/merge-requests/%s/head" % change.number
        change.branch = change.mr['target_branch']
        change.patchset = change.mr['sha']
        change.commit_id = change.mr['diff_refs'].get('head_sha')
        change.owner = change.mr['author'].get('username')
        # Files changes are not part of the Merge Request data
        # See api/merge_requests.html#get-single-mr-changes
        # this endpoint includes file changes information
        change.files = None
        change.title = change.mr['title']
        change.open = change.mr['state'] == 'opened'
        change.is_merged = change.mr['state'] == 'merged'
        # Can be "can_be_merged"
        change.merge_status = change.mr['merge_status']
        change.approved = change.mr['approved']
        change.message = change.mr['description']
        change.labels = change.mr['labels']
        change.updated_at = int(dateutil.parser.parse(
            change.mr['updated_at']).timestamp())
        log.info("Updated change from Gitlab %s" % change)

        if self.sched:
            self.sched.onChangeUpdated(change, event)

        return change

    def canMerge(self, change, allow_needs, event=None):
        log = get_annotated_logger(self.log, event)
        can_merge = True if change.merge_status == "can_be_merged" else False
        log.info('Check MR %s#%s mergeability can_merge: %s',
                 change.project.name, change.number, can_merge)
        return can_merge

    def getMR(self, project_name, number, event=None):
        log = get_annotated_logger(self.log, event)
        mr = self.gl_client.get_mr(project_name, number, zuul_event_id=event)
        log.info('Got MR %s#%s', project_name, number)
        mr_approval_status = self.gl_client.get_mr_approvals_status(
            project_name, number, zuul_event_id=event)
        log.info('Got MR approval status %s#%s', project_name, number)
        if 'approvals_left' in mr_approval_status:
            # 'approvals_left' is not present when 'Required Merge Request
            # Approvals' feature isn't available
            mr['approved'] = mr_approval_status['approvals_left'] == 0
        else:
            mr['approved'] = mr_approval_status['approved']
        return mr

    def commentMR(self, project_name, number, message, event=None):
        log = get_annotated_logger(self.log, event)
        self.gl_client.comment_mr(
            project_name, number, message, zuul_event_id=event)
        log.info("Commented on MR %s#%s", project_name, number)

    def approveMR(self, project_name, number, patchset, approve, event=None):
        log = get_annotated_logger(self.log, event)
        result = self.gl_client.approve_mr(
            project_name, number, patchset, approve, zuul_event_id=event)
        if result:
            log.info(
                "Set approval: %s on MR %s#%s (%s)", approve,
                project_name, number, patchset)

    def getChangesDependingOn(self, change, projects, tenant):
        """ Reverse lookup of MR depending on this one
        """
        # TODO(fbo): Further research to implement this lookup:
        # https://docs.gitlab.com/ee/api/search.html#scope-merge_requests
        # Will be done in a folloup commit
        return []

    def mergeMR(self, project_name, number, event=None):
        log = get_annotated_logger(self.log, event)
        self.gl_client.merge_mr(project_name, number, zuul_event_id=event)
        log.info("Merged MR %s#%s", project_name, number)


class GitlabWebController(BaseWebController):

    log = logging.getLogger("zuul.GitlabWebController")

    def __init__(self, zuul_web, connection):
        self.connection = connection
        self.zuul_web = zuul_web

    def _validate_token(self, headers):
        try:
            event_token = headers['x-gitlab-token']
        except KeyError:
            raise cherrypy.HTTPError(401, 'x-gitlab-token header missing.')

        configured_token = self.connection.webhook_token
        if not configured_token == event_token:
            self.log.debug(
                "Missmatch (Incoming token: %s, Configured token: %s)" % (
                    event_token, configured_token))
            raise cherrypy.HTTPError(
                401,
                'Token does not match the server side configured token')

    @cherrypy.expose
    @cherrypy.tools.json_out(content_type='application/json; charset=utf-8')
    def payload(self):
        headers = dict()
        for key, value in cherrypy.request.headers.items():
            headers[key.lower()] = value
        body = cherrypy.request.body.read()
        self.log.info("Event header: %s" % headers)
        self.log.info("Event body: %s" % body)
        self._validate_token(headers)
        json_payload = json.loads(body.decode('utf-8'))

        job = self.zuul_web.rpc.submitJob(
            'gitlab:%s:payload' % self.connection.connection_name,
            {'payload': json_payload})

        return json.loads(job.data[0])


def getSchema():
    return v.Any(str, v.Schema(dict))
