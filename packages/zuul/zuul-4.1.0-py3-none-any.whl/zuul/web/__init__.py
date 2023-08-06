# Copyright (c) 2017 Red Hat
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import cherrypy
import socket

from cachetools.func import ttl_cache
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
from ws4py.websocket import WebSocket
import codecs
import copy
from datetime import datetime
import json
import logging
import os
import time
import select
import threading

from zuul import exceptions
import zuul.lib.repl
from zuul.lib import commandsocket
from zuul.lib.re2util import filter_allowed_disallowed
import zuul.model
import zuul.rpcclient
from zuul.zk import ZooKeeperClient
from zuul.zk.components import ZooKeeperComponentRegistry
from zuul.zk.nodepool import ZooKeeperNodepool
from zuul.lib.auth import AuthenticatorRegistry
from zuul.lib.config import get_default

STATIC_DIR = os.path.join(os.path.dirname(__file__), 'static')
cherrypy.tools.websocket = WebSocketTool()

COMMANDS = ['stop', 'repl', 'norepl']


class SaveParamsTool(cherrypy.Tool):
    """
    Save the URL parameters to allow them to take precedence over query
    string parameters.
    """
    def __init__(self):
        cherrypy.Tool.__init__(self, 'on_start_resource',
                               self.saveParams)

    def _setup(self):
        cherrypy.Tool._setup(self)
        cherrypy.request.hooks.attach('before_handler',
                                      self.restoreParams)

    def saveParams(self, restore=True):
        cherrypy.request.url_params = cherrypy.request.params.copy()
        cherrypy.request.url_params_restore = restore

    def restoreParams(self):
        if cherrypy.request.url_params_restore:
            cherrypy.request.params.update(cherrypy.request.url_params)


cherrypy.tools.save_params = SaveParamsTool()


def handle_options(allowed_methods=None):
    if cherrypy.request.method == 'OPTIONS':
        methods = allowed_methods or ['GET', 'OPTIONS']
        if allowed_methods and 'OPTIONS' not in allowed_methods:
            methods = methods + ['OPTIONS']
        # discard decorated handler
        request = cherrypy.serving.request
        request.handler = None
        # Set CORS response headers
        resp = cherrypy.response
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.headers['Access-Control-Allow-Headers'] =\
            ', '.join(['Authorization', 'Content-Type'])
        resp.headers['Access-Control-Allow-Methods'] =\
            ', '.join(methods)
        # Allow caching of the preflight response
        resp.headers['Access-Control-Max-Age'] = 86400
        resp.status = 204


cherrypy.tools.handle_options = cherrypy.Tool('on_start_resource',
                                              handle_options)


class ChangeFilter(object):
    def __init__(self, desired):
        self.desired = desired

    def filterPayload(self, payload):
        status = []
        for pipeline in payload['pipelines']:
            for change_queue in pipeline['change_queues']:
                for head in change_queue['heads']:
                    for change in head:
                        if self.wantChange(change):
                            status.append(copy.deepcopy(change))
        return status

    def wantChange(self, change):
        return change['id'] == self.desired


class LogStreamHandler(WebSocket):
    log = logging.getLogger("zuul.web")

    def __init__(self, *args, **kw):
        kw['heartbeat_freq'] = 20
        super(LogStreamHandler, self).__init__(*args, **kw)
        self.streamer = None

    def received_message(self, message):
        if message.is_text:
            req = json.loads(message.data.decode('utf-8'))
            self.log.debug("Websocket request: %s", req)
            if self.streamer:
                self.log.debug("Ignoring request due to existing streamer")
                return
            try:
                self._streamLog(req)
            except Exception:
                self.log.exception("Error processing websocket message:")
                raise

    def closed(self, code, reason=None):
        self.log.debug("Websocket closed: %s %s", code, reason)
        if self.streamer:
            try:
                self.streamer.zuulweb.stream_manager.unregisterStreamer(
                    self.streamer)
            except Exception:
                self.log.exception("Error on remote websocket close:")

    def logClose(self, code, msg):
        self.log.debug("Websocket close: %s %s", code, msg)
        try:
            self.close(code, msg)
        except Exception:
            self.log.exception("Error closing websocket:")

    def _streamLog(self, request):
        """
        Stream the log for the requested job back to the client.

        :param dict request: The client request parameters.
        """
        for key in ('uuid', 'logfile'):
            if key not in request:
                return self.logClose(
                    4000,
                    "'{key}' missing from request payload".format(
                        key=key))

        port_location = self.zuulweb.rpc.get_job_log_stream_address(
            request['uuid'])
        if not port_location:
            return self.logClose(4011, "Error with Gearman")

        self.streamer = LogStreamer(
            self.zuulweb, self,
            port_location['server'], port_location['port'],
            request['uuid'])


class LogStreamer(object):
    log = logging.getLogger("zuul.web")

    def __init__(self, zuulweb, websocket, server, port, build_uuid):
        """
        Create a client to connect to the finger streamer and pull results.

        :param str server: The executor server running the job.
        :param str port: The executor server port.
        :param str build_uuid: The build UUID to stream.
        """
        self.log.debug("Connecting to finger server %s:%s", server, port)
        Decoder = codecs.getincrementaldecoder('utf8')
        self.decoder = Decoder()
        self.finger_socket = socket.create_connection(
            (server, port), timeout=10)
        self.finger_socket.settimeout(None)
        self.websocket = websocket
        self.zuulweb = zuulweb
        self.uuid = build_uuid
        msg = "%s\n" % build_uuid    # Must have a trailing newline!
        self.finger_socket.sendall(msg.encode('utf-8'))
        self.zuulweb.stream_manager.registerStreamer(self)

    def __repr__(self):
        return '<LogStreamer %s uuid:%s>' % (self.websocket, self.uuid)

    def errorClose(self):
        self.websocket.logClose(4011, "Unknown error")

    def handle(self, event):
        if event & select.POLLIN:
            data = self.finger_socket.recv(1024)
            if data:
                data = self.decoder.decode(data)
                if data:
                    self.websocket.send(data, False)
            else:
                # Make sure we flush anything left in the decoder
                data = self.decoder.decode(b'', final=True)
                if data:
                    self.websocket.send(data, False)
                self.zuulweb.stream_manager.unregisterStreamer(self)
                self.finger_socket.close()
                return self.websocket.logClose(1000, "No more data")
        else:
            self.zuulweb.stream_manager.unregisterStreamer(self)
            self.finger_socket.close()
            return self.websocket.logClose(1000, "Remote error")


class ZuulWebAPI(object):
    log = logging.getLogger("zuul.web")

    def __init__(self, zuulweb):
        self.rpc = zuulweb.rpc
        self.zk_client = zuulweb.zk_client
        self.zk_nodepool = ZooKeeperNodepool(self.zk_client)
        self.zuulweb = zuulweb
        self.cache = {}
        self.cache_time = {}
        self.cache_expiry = 1
        self.static_cache_expiry = zuulweb.static_cache_expiry
        self.status_lock = threading.Lock()

    def _basic_auth_header_check(self):
        """make sure protected endpoints have a Authorization header with the
        bearer token."""
        token = cherrypy.request.headers.get('Authorization', None)
        # Add basic checks here
        if token is None:
            status = 401
            e = 'Missing "Authorization" header'
            e_desc = e
        elif not token.lower().startswith('bearer '):
            status = 401
            e = 'Invalid Authorization header format'
            e_desc = '"Authorization" header must start with "Bearer"'
        else:
            return None
        error_header = '''Bearer realm="%s"
       error="%s"
       error_description="%s"''' % (self.zuulweb.authenticators.default_realm,
                                    e,
                                    e_desc)
        cherrypy.response.status = status
        cherrypy.response.headers["WWW-Authenticate"] = error_header
        return {'description': e_desc,
                'error': e,
                'realm': self.zuulweb.authenticators.default_realm}

    def _auth_token_check(self):
        rawToken = \
            cherrypy.request.headers['Authorization'][len('Bearer '):]
        try:
            claims = self.zuulweb.authenticators.authenticate(rawToken)
        except exceptions.AuthTokenException as e:
            for header, contents in e.getAdditionalHeaders().items():
                cherrypy.response.headers[header] = contents
            cherrypy.response.status = e.HTTPError
            return ({},
                    {'description': e.error_description,
                     'error': e.error,
                     'realm': e.realm})
        return (claims, None)

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out(content_type='application/json; charset=utf-8')
    @cherrypy.tools.handle_options(allowed_methods=['POST', ])
    def dequeue(self, tenant, project):
        basic_error = self._basic_auth_header_check()
        if basic_error is not None:
            return basic_error
        if cherrypy.request.method != 'POST':
            raise cherrypy.HTTPError(405)
        # AuthN/AuthZ
        claims, token_error = self._auth_token_check()
        if token_error is not None:
            return token_error
        self.is_authorized(claims, tenant)
        msg = 'User "%s" requesting "%s" on %s/%s'
        self.log.info(
            msg % (claims['__zuul_uid_claim'], 'dequeue',
                   tenant, project))

        body = cherrypy.request.json
        if 'pipeline' in body and (
            ('change' in body and 'ref' not in body) or
            ('change' not in body and 'ref' in body)):
            job = self.rpc.submitJob('zuul:dequeue',
                                     {'tenant': tenant,
                                      'pipeline': body['pipeline'],
                                      'project': project,
                                      'change': body.get('change', None),
                                      'ref': body.get('ref', None)})
            result = not job.failure
            resp = cherrypy.response
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return result
        else:
            raise cherrypy.HTTPError(400,
                                     'Invalid request body')

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out(content_type='application/json; charset=utf-8')
    @cherrypy.tools.handle_options(allowed_methods=['POST', ])
    def enqueue(self, tenant, project):
        basic_error = self._basic_auth_header_check()
        if basic_error is not None:
            return basic_error
        if cherrypy.request.method != 'POST':
            raise cherrypy.HTTPError(405)
        # AuthN/AuthZ
        claims, token_error = self._auth_token_check()
        if token_error is not None:
            return token_error
        self.is_authorized(claims, tenant)
        msg = 'User "%s" requesting "%s" on %s/%s'
        self.log.info(
            msg % (claims['__zuul_uid_claim'], 'enqueue',
                   tenant, project))

        body = cherrypy.request.json
        if all(p in body for p in ['change', 'pipeline']):
            return self._enqueue(tenant, project, **body)
        elif all(p in body for p in ['ref', 'oldrev',
                                     'newrev', 'pipeline']):
            return self._enqueue_ref(tenant, project, **body)
        else:
            raise cherrypy.HTTPError(400,
                                     'Invalid request body')

    def _enqueue(self, tenant, project, change, pipeline, **kwargs):
        job = self.rpc.submitJob('zuul:enqueue',
                                 {'tenant': tenant,
                                  'pipeline': pipeline,
                                  'project': project,
                                  'change': change, })
        result = not job.failure
        resp = cherrypy.response
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return result

    def _enqueue_ref(self, tenant, project, ref,
                     oldrev, newrev, pipeline, **kwargs):
        job = self.rpc.submitJob('zuul:enqueue_ref',
                                 {'tenant': tenant,
                                  'pipeline': pipeline,
                                  'project': project,
                                  'ref': ref,
                                  'oldrev': oldrev,
                                  'newrev': newrev, })
        result = not job.failure
        resp = cherrypy.response
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return result

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out(content_type='application/json; charset=utf-8')
    @cherrypy.tools.handle_options(allowed_methods=['POST', ])
    def promote(self, tenant):
        basic_error = self._basic_auth_header_check()
        if basic_error is not None:
            return basic_error
        if cherrypy.request.method != 'POST':
            raise cherrypy.HTTPError(405)
        # AuthN/AuthZ
        claims, token_error = self._auth_token_check()
        if token_error is not None:
            return token_error
        self.is_authorized(claims, tenant)

        body = cherrypy.request.json
        pipeline = body.get('pipeline')
        changes = body.get('changes')

        msg = 'User "%s" requesting "%s" on %s/%s'
        self.log.info(
            msg % (claims['__zuul_uid_claim'], 'promote',
                   tenant, pipeline))

        job = self.rpc.submitJob('zuul:promote',
                                 {
                                     'tenant': tenant,
                                     'pipeline': pipeline,
                                     'change_ids': changes,
                                 })
        result = not job.failure
        resp = cherrypy.response
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return result

    @cherrypy.expose
    @cherrypy.tools.json_out(content_type='application/json; charset=utf-8')
    def autohold_list(self, tenant, *args, **kwargs):
        # we don't use json_in because a payload is not mandatory with GET
        if cherrypy.request.method != 'GET':
            raise cherrypy.HTTPError(405)
        # filter by project if passed as a query string
        project = cherrypy.request.params.get('project', None)
        return self._autohold_list(tenant, project)

    @cherrypy.expose
    @cherrypy.tools.json_out(content_type='application/json; charset=utf-8')
    @cherrypy.tools.handle_options(allowed_methods=['GET', 'POST', ])
    def autohold(self, tenant, project=None):
        # we don't use json_in because a payload is not mandatory with GET
        # Note: GET handling is redundant with autohold_list
        # and could be removed.
        if cherrypy.request.method == 'GET':
            return self._autohold_list(tenant, project)
        elif cherrypy.request.method == 'POST':
            basic_error = self._basic_auth_header_check()
            if basic_error is not None:
                return basic_error
            # AuthN/AuthZ
            claims, token_error = self._auth_token_check()
            if token_error is not None:
                return token_error
            self.is_authorized(claims, tenant)
            msg = 'User "%s" requesting "%s" on %s/%s'
            self.log.info(
                msg % (claims['__zuul_uid_claim'], 'autohold',
                       tenant, project))

            length = int(cherrypy.request.headers['Content-Length'])
            body = cherrypy.request.body.read(length)
            try:
                jbody = json.loads(body.decode('utf-8'))
            except ValueError:
                raise cherrypy.HTTPError(406, 'JSON body required')
            if (jbody.get('change') and jbody.get('ref')):
                raise cherrypy.HTTPError(400,
                                         'change and ref are '
                                         'mutually exclusive')
            else:
                jbody['change'] = jbody.get('change', None)
                jbody['ref'] = jbody.get('ref', None)
            if all(p in jbody for p in ['job', 'change', 'ref',
                                        'count', 'reason',
                                        'node_hold_expiration']):
                data = {'tenant': tenant,
                        'project': project,
                        'job': jbody['job'],
                        'change': jbody['change'],
                        'ref': jbody['ref'],
                        'reason': jbody['reason'],
                        'count': jbody['count'],
                        'node_hold_expiration': jbody['node_hold_expiration']}
                result = self.rpc.submitJob('zuul:autohold', data)
                return not result.failure
            else:
                raise cherrypy.HTTPError(400,
                                         'Invalid request body')
        else:
            raise cherrypy.HTTPError(405)

    def _autohold_list(self, tenant, project=None):
        job = self.rpc.submitJob('zuul:autohold_list', {})
        if job.failure:
            raise cherrypy.HTTPError(500, 'autohold-list failed')
        else:
            payload = json.loads(job.data[0])
            result = []
            for request in payload:
                if tenant == request['tenant']:
                    if (project is None or
                            request['project'].endswith(project)):
                        result.append(
                            {'id': request['id'],
                             'tenant': request['tenant'],
                             'project': request['project'],
                             'job': request['job'],
                             'ref_filter': request['ref_filter'],
                             'max_count': request['max_count'],
                             'current_count': request['current_count'],
                             'reason': request['reason'],
                             'node_expiration': request['node_expiration'],
                             'expired': request['expired'],
                             'nodes': request['nodes']
                            })
            resp = cherrypy.response
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return result

    @cherrypy.expose
    @cherrypy.tools.json_out(content_type='application/json; charset=utf-8')
    @cherrypy.tools.handle_options(allowed_methods=['GET', 'DELETE', ])
    def autohold_by_request_id(self, tenant, request_id):
        if cherrypy.request.method == 'GET':
            return self._autohold_info(tenant, request_id)
        elif cherrypy.request.method == 'DELETE':
            return self._autohold_delete(tenant, request_id)
        else:
            raise cherrypy.HTTPError(405)

    def _autohold_info(self, tenant, request_id):
        job = self.rpc.submitJob('zuul:autohold_info',
                                 {'request_id': request_id})
        if job.failure:
            raise cherrypy.HTTPError(500, 'autohold-info failed')
        else:
            request = json.loads(job.data[0])
            if not request:
                raise cherrypy.HTTPError(
                    404, 'Hold request %s not found.' % request_id)
            if tenant != request['tenant']:
                # return 404 rather than 403 to avoid leaking tenant info
                raise cherrypy.HTTPError(
                    404, 'Hold request %s not found.' % request_id)
            resp = cherrypy.response
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return {
                'id': request['id'],
                'tenant': request['tenant'],
                'project': request['project'],
                'job': request['job'],
                'ref_filter': request['ref_filter'],
                'max_count': request['max_count'],
                'current_count': request['current_count'],
                'reason': request['reason'],
                'node_expiration': request['node_expiration'],
                'expired': request['expired'],
                'nodes': request['nodes']
            }

    def _autohold_delete(self, tenant, request_id):
        # We need tenant info from the request for authz
        request = self._autohold_info(tenant, request_id)
        basic_error = self._basic_auth_header_check()
        if basic_error is not None:
            return basic_error
        # AuthN/AuthZ
        claims, token_error = self._auth_token_check()
        if token_error is not None:
            return token_error
        self.is_authorized(claims, request['tenant'])
        msg = 'User "%s" requesting "%s" on %s/%s'
        self.log.info(
            msg % (claims['__zuul_uid_claim'], 'autohold-delete',
                   request['tenant'], request['project']))

        job = self.rpc.submitJob('zuul:autohold_delete',
                                 {'request_id': request_id})
        if job.failure:
            raise cherrypy.HTTPError(500, 'autohold-delete failed')

        cherrypy.response.status = 204

    @cherrypy.expose
    @cherrypy.tools.json_out(content_type='application/json; charset=utf-8')
    def index(self):
        return {
            'info': '/api/info',
            'connections': '/api/connections',
            'tenants': '/api/tenants',
            'tenant_info': '/api/tenant/{tenant}/info',
            'status': '/api/tenant/{tenant}/status',
            'status_change': '/api/tenant/{tenant}/status/change/{change}',
            'jobs': '/api/tenant/{tenant}/jobs',
            'job': '/api/tenant/{tenant}/job/{job_name}',
            'projects': '/api/tenant/{tenant}/projects',
            'project': '/api/tenant/{tenant}/project/{project:.*}',
            'project_freeze_jobs': '/api/tenant/{tenant}/pipeline/{pipeline}/'
                                   'project/{project:.*}/branch/{branch:.*}/'
                                   'freeze-jobs',
            'pipelines': '/api/tenant/{tenant}/pipelines',
            'labels': '/api/tenant/{tenant}/labels',
            'nodes': '/api/tenant/{tenant}/nodes',
            'key': '/api/tenant/{tenant}/key/{project:.*}.pub',
            'project_ssh_key': '/api/tenant/{tenant}/project-ssh-key/'
                               '{project:.*}.pub',
            'console_stream': '/api/tenant/{tenant}/console-stream',
            'badge': '/api/tenant/{tenant}/badge',
            'builds': '/api/tenant/{tenant}/builds',
            'build': '/api/tenant/{tenant}/build/{uuid}',
            'buildsets': '/api/tenant/{tenant}/buildsets',
            'buildset': '/api/tenant/{tenant}/buildset/{uuid}',
            'config_errors': '/api/tenant/{tenant}/config-errors',
            # TODO(mhu) remove after next release
            'authorizations': '/api/user/authorizations',
            'tenant_authorizations': ('/api/tenant/{tenant}'
                                      '/authorizations'),
            'autohold': '/api/tenant/{tenant}/project/{project:.*}/autohold',
            'autohold_list': '/api/tenant/{tenant}/autohold',
            'autohold_by_request_id': ('/api/tenant/{tenant}'
                                       '/autohold/{request_id}'),
            'autohold_delete': ('/api/tenant/{tenant}'
                                '/autohold/{request_id}'),
            'enqueue': '/api/tenant/{tenant}/project/{project:.*}/enqueue',
            'dequeue': '/api/tenant/{tenant}/project/{project:.*}/dequeue',
            'promote': '/api/tenant/{tenant}/promote',
        }

    @cherrypy.expose
    @cherrypy.tools.json_out(content_type='application/json; charset=utf-8')
    def info(self):
        return self._handleInfo(self.zuulweb.info)

    @cherrypy.expose
    @cherrypy.tools.save_params()
    @cherrypy.tools.json_out(content_type='application/json; charset=utf-8')
    def tenant_info(self, tenant):
        info = self.zuulweb.info.copy()
        info.tenant = tenant
        return self._handleInfo(info)

    def _handleInfo(self, info):
        ret = {'info': info.toDict()}
        resp = cherrypy.response
        resp.headers['Access-Control-Allow-Origin'] = '*'
        if self.static_cache_expiry:
            resp.headers['Cache-Control'] = "public, max-age=%d" % \
                self.static_cache_expiry
        resp.last_modified = self.zuulweb.start_time
        return ret

    def is_authorized(self, claims, tenant):
        # First, check for zuul.admin override
        override = claims.get('zuul', {}).get('admin', [])
        if (override == '*' or
            (isinstance(override, list) and tenant in override)):
            return True
        # Next, get the rules for tenant
        data = {'tenant': tenant, 'claims': claims}
        # TODO: it is probably worth caching
        job = self.rpc.submitJob('zuul:authorize_user', data)
        user_authz = json.loads(job.data[0])
        if not user_authz:
            raise cherrypy.HTTPError(403)
        return user_authz

    # TODO(mhu) deprecated, remove next version
    @cherrypy.expose
    @cherrypy.tools.json_out(content_type='application/json; charset=utf-8')
    @cherrypy.tools.handle_options(allowed_methods=['GET', ])
    def authorizations(self):
        basic_error = self._basic_auth_header_check()
        if basic_error is not None:
            return basic_error
        # AuthN/AuthZ
        claims, token_error = self._auth_token_check()
        if token_error is not None:
            return token_error
        try:
            admin_tenants = self._authorizations()
        except exceptions.AuthTokenException as e:
            for header, contents in e.getAdditionalHeaders().items():
                cherrypy.response.headers[header] = contents
            cherrypy.response.status = e.HTTPError
            return {'description': e.error_description,
                    'error': e.error,
                    'realm': e.realm}
        return {'zuul': {'admin': admin_tenants}, }

    @cherrypy.expose
    @cherrypy.tools.json_out(content_type='application/json; charset=utf-8')
    @cherrypy.tools.handle_options(allowed_methods=['GET', ])
    def tenant_authorizations(self, tenant):
        basic_error = self._basic_auth_header_check()
        if basic_error is not None:
            return basic_error
        # AuthN/AuthZ
        claims, token_error = self._auth_token_check()
        if token_error is not None:
            return token_error
        try:
            admin_tenants = self._authorizations()
        except exceptions.AuthTokenException as e:
            for header, contents in e.getAdditionalHeaders().items():
                cherrypy.response.headers[header] = contents
            cherrypy.response.status = e.HTTPError
            return {'description': e.error_description,
                    'error': e.error,
                    'realm': e.realm}
        return {'zuul': {'admin': tenant in admin_tenants,
                         'scope': [tenant, ]}, }

    # TODO good candidate for caching
    def _authorizations(self):
        rawToken = cherrypy.request.headers['Authorization'][len('Bearer '):]
        claims = self.zuulweb.authenticators.authenticate(rawToken)
        if 'zuul' in claims and 'admin' in claims.get('zuul', {}):
            return {'zuul': {'admin': claims['zuul']['admin']}, }
        job = self.rpc.submitJob('zuul:get_admin_tenants',
                                 {'claims': claims})
        admin_tenants = json.loads(job.data[0])
        return admin_tenants

    @ttl_cache(ttl=60)
    def _tenants(self):
        job = self.rpc.submitJob('zuul:tenant_list', {})
        return json.loads(job.data[0])

    @cherrypy.expose
    @cherrypy.tools.json_out(content_type='application/json; charset=utf-8')
    def tenants(self):
        ret = self._tenants()
        resp = cherrypy.response
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return ret

    @cherrypy.expose
    @cherrypy.tools.json_out(content_type='application/json; charset=utf-8')
    def connections(self):
        job = self.rpc.submitJob('zuul:connection_list', {})
        ret = json.loads(job.data[0])
        resp = cherrypy.response
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return ret

    def _getStatus(self, tenant):
        with self.status_lock:
            if tenant not in self.cache or \
               (time.time() - self.cache_time[tenant]) > self.cache_expiry:
                job = self.rpc.submitJob('zuul:status_get',
                                         {'tenant': tenant})
                self.cache[tenant] = json.loads(job.data[0])
                self.cache_time[tenant] = time.time()
        payload = self.cache[tenant]
        if payload.get('code') == 404:
            raise cherrypy.HTTPError(404, payload['message'])
        resp = cherrypy.response
        resp.headers["Cache-Control"] = "public, max-age=%d" % \
                                        self.cache_expiry
        last_modified = datetime.utcfromtimestamp(self.cache_time[tenant])
        last_modified_header = last_modified.strftime('%a, %d %b %Y %X GMT')
        resp.headers["Last-modified"] = last_modified_header
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return payload

    @cherrypy.expose
    @cherrypy.tools.save_params()
    @cherrypy.tools.json_out(content_type='application/json; charset=utf-8')
    def status(self, tenant):
        return self._getStatus(tenant)

    @cherrypy.expose
    @cherrypy.tools.save_params()
    @cherrypy.tools.json_out(content_type='application/json; charset=utf-8')
    def status_change(self, tenant, change):
        payload = self._getStatus(tenant)
        result_filter = ChangeFilter(change)
        return result_filter.filterPayload(payload)

    @cherrypy.expose
    @cherrypy.tools.save_params()
    @cherrypy.tools.json_out(content_type='application/json; charset=utf-8')
    def jobs(self, tenant):
        job = self.rpc.submitJob('zuul:job_list', {'tenant': tenant})
        ret = json.loads(job.data[0])
        if ret is None:
            raise cherrypy.HTTPError(404, 'Tenant %s does not exist.' % tenant)
        resp = cherrypy.response
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return ret

    @cherrypy.expose
    @cherrypy.tools.save_params()
    @cherrypy.tools.json_out(content_type='application/json; charset=utf-8')
    def config_errors(self, tenant):
        config_errors = self.rpc.submitJob(
            'zuul:config_errors_list', {'tenant': tenant})
        ret = json.loads(config_errors.data[0])
        if ret is None:
            raise cherrypy.HTTPError(404, 'Tenant %s does not exist.' % tenant)
        resp = cherrypy.response
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return ret

    @cherrypy.expose
    @cherrypy.tools.save_params()
    @cherrypy.tools.json_out(content_type='application/json; charset=utf-8')
    def job(self, tenant, job_name):
        job = self.rpc.submitJob(
            'zuul:job_get', {'tenant': tenant, 'job': job_name})
        ret = json.loads(job.data[0])
        if not ret:
            raise cherrypy.HTTPError(404, 'Job %s does not exist.' % job_name)
        resp = cherrypy.response
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return ret

    @cherrypy.expose
    @cherrypy.tools.save_params()
    @cherrypy.tools.json_out(content_type='application/json; charset=utf-8')
    def projects(self, tenant):
        job = self.rpc.submitJob('zuul:project_list', {'tenant': tenant})
        ret = json.loads(job.data[0])
        if ret is None:
            raise cherrypy.HTTPError(404, 'Tenant %s does not exist.' % tenant)
        resp = cherrypy.response
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return ret

    @cherrypy.expose
    @cherrypy.tools.save_params()
    @cherrypy.tools.json_out(content_type='application/json; charset=utf-8')
    def project(self, tenant, project):
        job = self.rpc.submitJob(
            'zuul:project_get', {'tenant': tenant, 'project': project})
        ret = json.loads(job.data[0])
        if ret is None:
            raise cherrypy.HTTPError(404, 'Tenant %s does not exist.' % tenant)
        if not ret:
            raise cherrypy.HTTPError(
                404, 'Project %s does not exist.' % project)
        resp = cherrypy.response
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return ret

    @cherrypy.expose
    @cherrypy.tools.save_params()
    @cherrypy.tools.json_out(content_type='application/json; charset=utf-8')
    def pipelines(self, tenant):
        job = self.rpc.submitJob('zuul:pipeline_list', {'tenant': tenant})
        ret = json.loads(job.data[0])
        if ret is None:
            raise cherrypy.HTTPError(404, 'Tenant %s does not exist.' % tenant)
        resp = cherrypy.response
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return ret

    @cherrypy.expose
    @cherrypy.tools.save_params()
    @cherrypy.tools.json_out(content_type='application/json; charset=utf-8')
    def labels(self, tenant):
        job = self.rpc.submitJob('zuul:allowed_labels_get', {'tenant': tenant})
        data = json.loads(job.data[0])
        if data is None:
            raise cherrypy.HTTPError(404, 'Tenant %s does not exist.' % tenant)
        # TODO(jeblair): The first case can be removed after 3.16.0 is
        # released.
        if isinstance(data, list):
            allowed_labels = data
            disallowed_labels = []
        else:
            allowed_labels = data['allowed_labels']
            disallowed_labels = data['disallowed_labels']
        labels = set()
        for launcher in self.zk_nodepool.getRegisteredLaunchers():
            labels.update(filter_allowed_disallowed(
                launcher.supported_labels,
                allowed_labels, disallowed_labels))
        ret = [{'name': label} for label in sorted(labels)]
        resp = cherrypy.response
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return ret

    @cherrypy.expose
    @cherrypy.tools.save_params()
    @cherrypy.tools.json_out(content_type='application/json; charset=utf-8')
    def nodes(self, tenant):
        ret = []
        for node in self.zk_nodepool.nodeIterator():
            node_data = {}
            for key in ("id", "type", "connection_type", "external_id",
                        "provider", "state", "state_time", "comment"):
                node_data[key] = node.get(key)
            ret.append(node_data)
        resp = cherrypy.response
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return ret

    @cherrypy.expose
    @cherrypy.tools.save_params()
    def key(self, tenant, project):
        job = self.rpc.submitJob('zuul:key_get', {'tenant': tenant,
                                                  'project': project,
                                                  'key': 'secrets'})
        if not job.data:
            raise cherrypy.HTTPError(
                404, 'Project %s does not exist.' % project)
        resp = cherrypy.response
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.headers['Content-Type'] = 'text/plain'
        return job.data[0]

    @cherrypy.expose
    @cherrypy.tools.save_params()
    def project_ssh_key(self, tenant, project):
        job = self.rpc.submitJob('zuul:key_get', {'tenant': tenant,
                                                  'project': project,
                                                  'key': 'ssh'})
        if not job.data:
            raise cherrypy.HTTPError(
                404, 'Project %s does not exist.' % project)
        resp = cherrypy.response
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.headers['Content-Type'] = 'text/plain'
        return job.data[0] + '\n'

    def buildToDict(self, build, buildset=None):
        start_time = build.start_time
        if build.start_time:
            start_time = start_time.strftime(
                '%Y-%m-%dT%H:%M:%S')
        end_time = build.end_time
        if build.end_time:
            end_time = end_time.strftime(
                '%Y-%m-%dT%H:%M:%S')
        if build.start_time and build.end_time:
            duration = (build.end_time -
                        build.start_time).total_seconds()
        else:
            duration = None

        ret = {
            'uuid': build.uuid,
            'job_name': build.job_name,
            'result': build.result,
            'held': build.held,
            'start_time': start_time,
            'end_time': end_time,
            'duration': duration,
            'voting': build.voting,
            'log_url': build.log_url,
            'node_name': build.node_name,
            'error_detail': build.error_detail,
            'final': build.final,
            'artifacts': [],
            'provides': [],
        }

        if buildset:
            ret.update({
                'project': buildset.project,
                'branch': buildset.branch,
                'pipeline': buildset.pipeline,
                'change': buildset.change,
                'patchset': buildset.patchset,
                'ref': buildset.ref,
                'newrev': buildset.newrev,
                'ref_url': buildset.ref_url,
                'event_id': buildset.event_id,
                'buildset': {
                    'uuid': buildset.uuid,
                },
            })

        for artifact in build.artifacts:
            art = {
                'name': artifact.name,
                'url': artifact.url,
            }
            if artifact.meta:
                art['metadata'] = json.loads(artifact.meta)
            ret['artifacts'].append(art)
        for provides in build.provides:
            ret['provides'].append({
                'name': provides.name,
            })
        return ret

    def _get_connection(self):
        return self.zuulweb.connections.connections['database']

    @cherrypy.expose
    @cherrypy.tools.save_params()
    @cherrypy.tools.json_out(content_type='application/json; charset=utf-8')
    def builds(self, tenant, project=None, pipeline=None, change=None,
               branch=None, patchset=None, ref=None, newrev=None,
               uuid=None, job_name=None, voting=None, node_name=None,
               result=None, final=None, held=None, limit=50, skip=0):
        connection = self._get_connection()

        if tenant not in [x['name'] for x in self._tenants()]:
            raise cherrypy.HTTPError(404, 'Tenant %s does not exist.' % tenant)

        # If final is None, we return all builds, both final and non-final
        if final is not None:
            final = final.lower() == "true"

        builds = connection.getBuilds(
            tenant=tenant, project=project, pipeline=pipeline, change=change,
            branch=branch, patchset=patchset, ref=ref, newrev=newrev,
            uuid=uuid, job_name=job_name, voting=voting, node_name=node_name,
            result=result, final=final, held=held, limit=limit, offset=skip)

        resp = cherrypy.response
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return [self.buildToDict(b, b.buildset) for b in builds]

    @cherrypy.expose
    @cherrypy.tools.save_params()
    @cherrypy.tools.json_out(content_type='application/json; charset=utf-8')
    def build(self, tenant, uuid):
        connection = self._get_connection()

        data = connection.getBuilds(tenant=tenant, uuid=uuid, limit=1)
        if not data:
            raise cherrypy.HTTPError(404, "Build not found")
        data = self.buildToDict(data[0], data[0].buildset)
        resp = cherrypy.response
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return data

    def buildsetToDict(self, buildset, builds=[]):
        ret = {
            'uuid': buildset.uuid,
            'result': buildset.result,
            'message': buildset.message,
            'project': buildset.project,
            'branch': buildset.branch,
            'pipeline': buildset.pipeline,
            'change': buildset.change,
            'patchset': buildset.patchset,
            'ref': buildset.ref,
            'newrev': buildset.newrev,
            'ref_url': buildset.ref_url,
            'event_id': buildset.event_id,
        }
        if builds:
            ret['builds'] = []
            ret['retry_builds'] = []
        for build in builds:
            # Put all non-final (retry) builds under a different key
            if not build.final:
                ret['retry_builds'].append(self.buildToDict(build))
            else:
                ret['builds'].append(self.buildToDict(build))
        return ret

    @cherrypy.expose
    @cherrypy.tools.save_params()
    def badge(self, tenant, project=None, pipeline=None, branch=None):
        connection = self._get_connection()

        buildsets = connection.getBuildsets(
            tenant=tenant, project=project, pipeline=pipeline,
            branch=branch, limit=1)
        if not buildsets:
            raise cherrypy.HTTPError(404, 'No buildset found')

        if buildsets[0].result == 'SUCCESS':
            file = 'passing.svg'
        else:
            file = 'failing.svg'
        path = os.path.join(self.zuulweb.static_path, file)

        # Ensure the badge are not cached
        cherrypy.response.headers['Cache-Control'] = "no-cache"

        return cherrypy.lib.static.serve_file(
            path=path, content_type="image/svg+xml")

    @cherrypy.expose
    @cherrypy.tools.save_params()
    @cherrypy.tools.json_out(content_type='application/json; charset=utf-8')
    def buildsets(self, tenant, project=None, pipeline=None, change=None,
                  branch=None, patchset=None, ref=None, newrev=None,
                  uuid=None, result=None, limit=50, skip=0):
        connection = self._get_connection()

        buildsets = connection.getBuildsets(
            tenant=tenant, project=project, pipeline=pipeline, change=change,
            branch=branch, patchset=patchset, ref=ref, newrev=newrev,
            uuid=uuid, result=result,
            limit=limit, offset=skip)

        resp = cherrypy.response
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return [self.buildsetToDict(b) for b in buildsets]

    @cherrypy.expose
    @cherrypy.tools.save_params()
    @cherrypy.tools.json_out(content_type='application/json; charset=utf-8')
    def buildset(self, tenant, uuid):
        connection = self._get_connection()

        data = connection.getBuildset(tenant, uuid)
        if not data:
            raise cherrypy.HTTPError(404, "Buildset not found")
        data = self.buildsetToDict(data, data.builds)
        resp = cherrypy.response
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return data

    @cherrypy.expose
    @cherrypy.tools.save_params()
    @cherrypy.tools.websocket(handler_cls=LogStreamHandler)
    def console_stream(self, tenant):
        cherrypy.request.ws_handler.zuulweb = self.zuulweb

    @cherrypy.expose
    @cherrypy.tools.save_params()
    @cherrypy.tools.json_out(content_type='application/json; charset=utf-8')
    def project_freeze_jobs(self, tenant, pipeline, project, branch):
        job = self.rpc.submitJob(
            'zuul:project_freeze_jobs',
            {
                'tenant': tenant,
                'project': project,
                'pipeline': pipeline,
                'branch': branch
            }
        )
        ret = json.loads(job.data[0])
        if not ret:
            raise cherrypy.HTTPError(404)
        resp = cherrypy.response
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return ret


class StaticHandler(object):
    def __init__(self, root):
        self.root = root

    def default(self, path, **kwargs):
        # Try to handle static file first
        handled = cherrypy.lib.static.staticdir(
            section="",
            dir=self.root,
            index='index.html')
        if not path or not handled:
            # When not found, serve the index.html
            return cherrypy.lib.static.serve_file(
                path=os.path.join(self.root, "index.html"),
                content_type="text/html")
        else:
            return cherrypy.lib.static.serve_file(
                path=os.path.join(self.root, path))


class StreamManager(object):
    log = logging.getLogger("zuul.web")

    def __init__(self):
        self.streamers = {}
        self.poll = select.poll()
        self.bitmask = (select.POLLIN | select.POLLERR |
                        select.POLLHUP | select.POLLNVAL)
        self.wake_read, self.wake_write = os.pipe()
        self.poll.register(self.wake_read, self.bitmask)

    def start(self):
        self._stopped = False
        self.thread = threading.Thread(
            target=self.run,
            name='StreamManager')
        self.thread.start()

    def stop(self):
        self._stopped = True
        os.write(self.wake_write, b'\n')
        self.thread.join()

    def run(self):
        while True:
            for fd, event in self.poll.poll():
                if self._stopped:
                    return
                if fd == self.wake_read:
                    os.read(self.wake_read, 1024)
                    continue
                streamer = self.streamers.get(fd)
                if streamer:
                    try:
                        streamer.handle(event)
                    except Exception:
                        self.log.exception("Error in streamer:")
                        streamer.errorClose()
                        self.unregisterStreamer(streamer)
                else:
                    try:
                        self.poll.unregister(fd)
                    except KeyError:
                        pass

    def registerStreamer(self, streamer):
        self.log.debug("Registering streamer %s", streamer)
        self.streamers[streamer.finger_socket.fileno()] = streamer
        self.poll.register(streamer.finger_socket.fileno(), self.bitmask)
        os.write(self.wake_write, b'\n')

    def unregisterStreamer(self, streamer):
        self.log.debug("Unregistering streamer %s", streamer)
        try:
            self.poll.unregister(streamer.finger_socket)
        except KeyError:
            pass
        try:
            del self.streamers[streamer.finger_socket.fileno()]
        except KeyError:
            pass


class ZuulWeb(object):
    log = logging.getLogger("zuul.web.ZuulWeb")

    def __init__(self,
                 config,
                 connections,
                 authenticators: AuthenticatorRegistry,
                 info: zuul.model.WebInfo = None):
        self.start_time = time.time()
        self.config = config
        self.listen_address = get_default(self.config,
                                          'web', 'listen_address',
                                          '127.0.0.1')
        self.listen_port = get_default(self.config, 'web', 'port', 9000)
        self.server = None
        self.static_cache_expiry = get_default(self.config, 'web',
                                               'static_cache_expiry',
                                               3600)
        self.info = info
        self.static_path = os.path.abspath(
            get_default(self.config, 'web', 'static_path', STATIC_DIR)
        )
        self.hostname = socket.getfqdn()

        gear_server = get_default(self.config, 'gearman', 'server')
        gear_port = get_default(self.config, 'gearman', 'port', 4730)
        ssl_key = get_default(self.config, 'gearman', 'ssl_key')
        ssl_cert = get_default(self.config, 'gearman', 'ssl_cert')
        ssl_ca = get_default(self.config, 'gearman', 'ssl_ca')

        # instanciate handlers
        self.rpc = zuul.rpcclient.RPCClient(gear_server, gear_port,
                                            ssl_key, ssl_cert, ssl_ca,
                                            client_id='Zuul Web Server')
        self.zk_client = ZooKeeperClient.fromConfig(self.config)
        self.zk_client.connect()
        self.zk_component = (
            ZooKeeperComponentRegistry(self.zk_client).register(
                'webs', self.hostname
            )
        )

        self.connections = connections
        self.authenticators = authenticators
        self.stream_manager = StreamManager()

        command_socket = get_default(
            self.config, 'web', 'command_socket',
            '/var/lib/zuul/web.socket'
        )

        self.command_socket = commandsocket.CommandSocket(command_socket)

        self.repl = None

        self.command_map = {
            'stop': self.stop,
            'repl': self.start_repl,
            'norepl': self.stop_repl,
        }

        route_map = cherrypy.dispatch.RoutesDispatcher()
        api = ZuulWebAPI(self)
        route_map.connect('api', '/api',
                          controller=api, action='index')
        route_map.connect('api', '/api/info',
                          controller=api, action='info')
        route_map.connect('api', '/api/connections',
                          controller=api, action='connections')
        route_map.connect('api', '/api/tenants',
                          controller=api, action='tenants')
        route_map.connect('api', '/api/tenant/{tenant}/info',
                          controller=api, action='tenant_info')
        route_map.connect('api', '/api/tenant/{tenant}/status',
                          controller=api, action='status')
        route_map.connect('api', '/api/tenant/{tenant}/status/change/{change}',
                          controller=api, action='status_change')
        route_map.connect('api', '/api/tenant/{tenant}/jobs',
                          controller=api, action='jobs')
        route_map.connect('api', '/api/tenant/{tenant}/job/{job_name}',
                          controller=api, action='job')
        # if no auth configured, deactivate admin routes
        if self.authenticators.authenticators:
            # route order is important, put project actions before the more
            # generic tenant/{tenant}/project/{project} route
            route_map.connect('api', '/api/user/authorizations',
                              controller=api, action='authorizations')
            route_map.connect('api', '/api/tenant/{tenant}/authorizations',
                              controller=api,
                              action='tenant_authorizations')
            route_map.connect('api', '/api/tenant/{tenant}/promote',
                              controller=api, action='promote')
            route_map.connect(
                'api',
                '/api/tenant/{tenant}/project/{project:.*}/autohold',
                controller=api, action='autohold')
            route_map.connect(
                'api',
                '/api/tenant/{tenant}/project/{project:.*}/enqueue',
                controller=api, action='enqueue')
            route_map.connect(
                'api',
                '/api/tenant/{tenant}/project/{project:.*}/dequeue',
                controller=api, action='dequeue')
        route_map.connect('api', '/api/tenant/{tenant}/autohold/{request_id}',
                          controller=api,
                          action='autohold_by_request_id')
        route_map.connect('api', '/api/tenant/{tenant}/autohold',
                          controller=api, action='autohold_list')
        route_map.connect('api', '/api/tenant/{tenant}/projects',
                          controller=api, action='projects')
        route_map.connect('api', '/api/tenant/{tenant}/project/{project:.*}',
                          controller=api, action='project')
        route_map.connect(
            'api',
            '/api/tenant/{tenant}/pipeline/{pipeline}'
            '/project/{project:.*}/branch/{branch:.*}/freeze-jobs',
            controller=api, action='project_freeze_jobs'
        )
        route_map.connect('api', '/api/tenant/{tenant}/pipelines',
                          controller=api, action='pipelines')
        route_map.connect('api', '/api/tenant/{tenant}/labels',
                          controller=api, action='labels')
        route_map.connect('api', '/api/tenant/{tenant}/nodes',
                          controller=api, action='nodes')
        route_map.connect('api', '/api/tenant/{tenant}/key/{project:.*}.pub',
                          controller=api, action='key')
        route_map.connect('api', '/api/tenant/{tenant}/'
                          'project-ssh-key/{project:.*}.pub',
                          controller=api, action='project_ssh_key')
        route_map.connect('api', '/api/tenant/{tenant}/console-stream',
                          controller=api, action='console_stream')
        route_map.connect('api', '/api/tenant/{tenant}/builds',
                          controller=api, action='builds')
        route_map.connect('api', '/api/tenant/{tenant}/badge',
                          controller=api, action='badge')
        route_map.connect('api', '/api/tenant/{tenant}/build/{uuid}',
                          controller=api, action='build')
        route_map.connect('api', '/api/tenant/{tenant}/buildsets',
                          controller=api, action='buildsets')
        route_map.connect('api', '/api/tenant/{tenant}/buildset/{uuid}',
                          controller=api, action='buildset')
        route_map.connect('api', '/api/tenant/{tenant}/config-errors',
                          controller=api, action='config_errors')

        for connection in connections.connections.values():
            controller = connection.getWebController(self)
            if controller:
                cherrypy.tree.mount(
                    controller,
                    '/api/connection/%s' % connection.connection_name)

        # Add fallthrough routes at the end for the static html/js files
        route_map.connect(
            'root_static', '/{path:.*}',
            controller=StaticHandler(self.static_path),
            action='default')

        conf = {
            '/': {
                'request.dispatch': route_map
            }
        }
        cherrypy.config.update({
            'global': {
                'environment': 'production',
                'server.socket_host': self.listen_address,
                'server.socket_port': int(self.listen_port),
            },
        })

        cherrypy.tree.mount(api, '/', config=conf)

    @property
    def port(self):
        return cherrypy.server.bound_addr[1]

    def start(self):
        self.log.debug("ZuulWeb starting")
        self.stream_manager.start()
        self.wsplugin = WebSocketPlugin(cherrypy.engine)
        self.wsplugin.subscribe()
        cherrypy.engine.start()

        self.log.debug("Starting command processor")
        self._command_running = True
        self.command_socket.start()
        self.command_thread = threading.Thread(target=self.runCommand,
                                               name='command')
        self.command_thread.daemon = True
        self.command_thread.start()
        self.zk_component.set('state', self.zk_component.RUNNING)

    def stop(self):
        self.log.debug("ZuulWeb stopping")
        self.zk_component.set('state', self.zk_component.STOPPED)
        self.rpc.shutdown()
        cherrypy.engine.exit()
        # Not strictly necessary, but without this, if the server is
        # started again (e.g., in the unit tests) it will reuse the
        # same host/port settings.
        cherrypy.server.httpserver = None
        self.wsplugin.unsubscribe()
        self.stream_manager.stop()
        self.zk_client.disconnect()
        self.stop_repl()
        self._command_running = False
        self.command_socket.stop()
        self.command_thread.join()

    def join(self):
        self.command_thread.join()

    def runCommand(self):
        while self._command_running:
            try:
                command = self.command_socket.get().decode('utf8')
                if command != '_stop':
                    self.command_map[command]()
            except Exception:
                self.log.exception("Exception while processing command")

    def start_repl(self):
        if self.repl:
            return
        self.repl = zuul.lib.repl.REPLServer(self)
        self.repl.start()

    def stop_repl(self):
        if not self.repl:
            return
        self.repl.stop()
        self.repl = None
