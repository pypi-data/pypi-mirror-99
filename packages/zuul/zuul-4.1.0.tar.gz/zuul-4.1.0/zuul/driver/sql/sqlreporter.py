# Copyright 2015 Rackspace Australia
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

import datetime
import json
import logging
import time
import voluptuous as v

from zuul.lib.logutil import get_annotated_logger
from zuul.lib.result_data import get_artifacts_from_result_data
from zuul.reporter import BaseReporter


class SQLReporter(BaseReporter):
    """Sends off reports to a database."""

    name = 'sql'
    log = logging.getLogger("zuul.SQLReporter")

    def _getBuildData(self, item, job, build):
        (result, _) = item.formatJobResult(job, build)
        start = end = None
        if build.start_time:
            start = datetime.datetime.fromtimestamp(
                build.start_time,
                tz=datetime.timezone.utc)
        if build.end_time:
            end = datetime.datetime.fromtimestamp(
                build.end_time,
                tz=datetime.timezone.utc)
        return result, build.log_url, start, end

    def createBuildEntry(self, item, job, db_buildset, build, final=True):
        # Ensure end_time is defined
        if not build.end_time:
            build.end_time = time.time()

        result, log_url, start, end = self._getBuildData(item, job, build)
        db_build = db_buildset.createBuild(
            uuid=build.uuid,
            job_name=build.job.name,
            result=result,
            start_time=start,
            end_time=end,
            voting=build.job.voting,
            log_url=log_url,
            node_name=build.node_name,
            error_detail=build.error_detail,
            final=final,
            held=build.held,
        )

        return db_build

    def report(self, item):
        """Create an entry into a database."""
        log = get_annotated_logger(self.log, item.event)

        if not self.connection.tables_established:
            log.warning("SQL reporter (%s) is disabled ", self)
            return

        event_id = None
        if item.event is not None:
            event_id = getattr(item.event, "zuul_event_id", None)

        with self.connection.getSession() as db:
            db_buildset = db.createBuildSet(
                uuid=item.current_build_set.uuid,
                tenant=item.pipeline.tenant.name,
                pipeline=item.pipeline.name,
                project=item.change.project.name,
                change=getattr(item.change, 'number', None),
                patchset=getattr(item.change, 'patchset', None),
                ref=getattr(item.change, 'ref', ''),
                oldrev=getattr(item.change, 'oldrev', ''),
                newrev=getattr(item.change, 'newrev', ''),
                branch=getattr(item.change, 'branch', ''),
                zuul_ref=item.current_build_set.ref,
                ref_url=item.change.url,
                result=item.current_build_set.result,
                event_id=event_id,
                message=self._formatItemReport(item, with_jobs=False),
            )
            for job in item.getJobs():
                build = item.current_build_set.getBuild(job.name)
                if not build:
                    # build hasn't begun. The sql reporter can only send back
                    # stats about builds. It doesn't understand how to store
                    # information about the change.
                    continue
                retry_builds = item.current_build_set.getRetryBuildsForJob(
                    job.name
                )
                for retry_build in retry_builds:
                    self.createBuildEntry(
                        item, job, db_buildset, retry_build, final=False
                    )

                db_build = self.createBuildEntry(item, job, db_buildset, build)

                for provides in job.provides:
                    db_build.createProvides(name=provides)

                for artifact in get_artifacts_from_result_data(
                    build.result_data,
                    logger=self.log):
                    if 'metadata' in artifact:
                        artifact['metadata'] = json.dumps(artifact['metadata'])
                    db_build.createArtifact(**artifact)


def getSchema():
    sql_reporter = v.Schema(None)
    return sql_reporter
