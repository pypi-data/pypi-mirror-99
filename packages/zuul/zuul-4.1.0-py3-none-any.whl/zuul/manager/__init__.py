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
import collections
import logging
import textwrap
import time
import urllib
from abc import ABCMeta, abstractmethod

from zuul import exceptions
from zuul import model
from zuul.lib.dependson import find_dependency_headers
from zuul.lib.logutil import get_annotated_logger
from zuul.lib.tarjan import strongly_connected_components
from zuul.model import QueueItem


class DynamicChangeQueueContextManager(object):
    def __init__(self, change_queue):
        self.change_queue = change_queue

    def __enter__(self):
        return self.change_queue

    def __exit__(self, etype, value, tb):
        if self.change_queue and not self.change_queue.queue:
            self.change_queue.pipeline.removeQueue(self.change_queue)


class StaticChangeQueueContextManager(object):
    def __init__(self, change_queue):
        self.change_queue = change_queue

    def __enter__(self):
        return self.change_queue

    def __exit__(self, etype, value, tb):
        pass


class PipelineManager(metaclass=ABCMeta):
    """Abstract Base Class for enqueing and processing Changes in a Pipeline"""

    def __init__(self, sched, pipeline):
        self.log = logging.getLogger("zuul.Pipeline.%s.%s" %
                                     (pipeline.tenant.name,
                                      pipeline.name,))
        self.sched = sched
        self.pipeline = pipeline
        self.event_filters = []
        self.ref_filters = []

    def __str__(self):
        return "<%s %s>" % (self.__class__.__name__, self.pipeline.name)

    def _postConfig(self, layout):
        # All pipelines support shared queues for setting
        # relative_priority; only the dependent pipeline uses them for
        # pipeline queing.
        self.buildChangeQueues(layout)

    def buildChangeQueues(self, layout):
        self.log.debug("Building relative_priority queues")
        change_queues = self.pipeline.relative_priority_queues
        tenant = self.pipeline.tenant
        layout_project_configs = layout.project_configs

        for project_name, project_configs in layout_project_configs.items():
            (trusted, project) = tenant.getProject(project_name)
            project_queue_name = None
            pipeline_queue_name = None
            project_in_pipeline = False
            for project_config in layout.getAllProjectConfigs(project_name):
                project_pipeline_config = project_config.pipelines.get(
                    self.pipeline.name)
                if project_pipeline_config is None:
                    continue
                project_in_pipeline = True
                if not pipeline_queue_name:
                    pipeline_queue_name = project_pipeline_config.queue_name
                if not project_queue_name:
                    project_queue_name = project_config.queue_name
            if not project_in_pipeline:
                continue

            # Note: we currently support queue name per pipeline and per
            # project while project has precedence.
            queue_name = project_queue_name or pipeline_queue_name

            if not queue_name:
                continue
            if queue_name in change_queues:
                change_queue = change_queues[queue_name]
            else:
                change_queue = []
                change_queues[queue_name] = change_queue
                self.log.debug("Created queue: %s" % queue_name)
            change_queue.append(project)
            self.log.debug("Added project %s to queue: %s" %
                           (project, queue_name))

    def getSubmitAllowNeeds(self):
        # Get a list of code review labels that are allowed to be
        # "needed" in the submit records for a change, with respect
        # to this queue.  In other words, the list of review labels
        # this queue itself is likely to set before submitting.
        allow_needs = set()
        for action_reporter in self.pipeline.success_actions:
            allow_needs.update(action_reporter.getSubmitAllowNeeds())
        return allow_needs

    def eventMatches(self, event, change):
        log = get_annotated_logger(self.log, event)
        if event.forced_pipeline:
            if event.forced_pipeline == self.pipeline.name:
                log.debug("Event %s for change %s was directly assigned "
                          "to pipeline %s" % (event, change, self))
                return True
            else:
                return False
        for ef in self.event_filters:
            match_result = ef.matches(event, change)
            if match_result:
                log.debug("Event %s for change %s matched %s "
                          "in pipeline %s" % (event, change, ef, self))
                return True
            else:
                log.debug("Event %s for change %s does not match %s "
                          "in pipeline %s because %s" % (
                              event, change, ef, self, str(match_result)))
        return False

    def getNodePriority(self, item):
        queue = self.pipeline.getRelativePriorityQueue(item.change.project)
        items = self.pipeline.getAllItems()
        items = [i for i in items
                 if i.change.project in queue and
                 i.live]
        return items.index(item)

    def isChangeAlreadyInPipeline(self, change):
        # Checks live items in the pipeline
        for item in self.pipeline.getAllItems():
            if item.live and change.equals(item.change):
                return True
        return False

    def isChangeAlreadyInQueue(self, change, change_queue):
        # Checks any item in the specified change queue
        for item in change_queue.queue:
            if change.equals(item.change):
                return True
        return False

    def reportEnqueue(self, item):
        if not self.pipeline._disabled:
            self.log.info("Reporting enqueue, action %s item %s" %
                          (self.pipeline.enqueue_actions, item))
            ret = self.sendReport(self.pipeline.enqueue_actions, item)
            if ret:
                self.log.error("Reporting item enqueued %s received: %s" %
                               (item, ret))

    def reportStart(self, item):
        if not self.pipeline._disabled:
            self.log.info("Reporting start, action %s item %s" %
                          (self.pipeline.start_actions, item))
            ret = self.sendReport(self.pipeline.start_actions, item)
            if ret:
                self.log.error("Reporting item start %s received: %s" %
                               (item, ret))

    def reportDequeue(self, item):
        if not self.pipeline._disabled:
            self.log.info(
                "Reporting dequeue, action %s item%s",
                self.pipeline.dequeue_actions,
                item,
            )
            ret = self.sendReport(self.pipeline.dequeue_actions, item)
            if ret:
                self.log.error(
                    "Reporting item dequeue %s received: %s", item, ret
                )

    def sendReport(self, action_reporters, item, message=None):
        """Sends the built message off to configured reporters.

        Takes the action_reporters, item, message and extra options and
        sends them to the pluggable reporters.
        """
        log = get_annotated_logger(self.log, item.event)
        report_errors = []
        if len(action_reporters) > 0:
            for reporter in action_reporters:
                try:
                    ret = reporter.report(item)
                    if ret:
                        report_errors.append(ret)
                except Exception as e:
                    item.setReportedResult('ERROR')
                    log.exception("Exception while reporting")
                    report_errors.append(str(e))
        return report_errors

    def isChangeReadyToBeEnqueued(self, change, event):
        return True

    def enqueueChangesAhead(self, change, event, quiet, ignore_requirements,
                            change_queue, history=None, dependency_graph=None):
        return True

    def enqueueChangesBehind(self, change, event, quiet, ignore_requirements,
                             change_queue, history=None,
                             dependency_graph=None):
        return True

    def checkForChangesNeededBy(self, change, change_queue, event,
                                dependency_graph=None):
        return True

    def getFailingDependentItems(self, item):
        return None

    def getItemForChange(self, change, change_queue=None):
        if change_queue is not None:
            items = change_queue.queue
        else:
            items = self.pipeline.getAllItems()

        for item in items:
            if item.change.equals(change):
                return item
        return None

    def findOldVersionOfChangeAlreadyInQueue(self, change):
        for item in self.pipeline.getAllItems():
            if not item.live:
                continue
            if change.isUpdateOf(item.change):
                return item
        return None

    def removeOldVersionsOfChange(self, change, event):
        if not self.pipeline.dequeue_on_new_patchset:
            return
        old_item = self.findOldVersionOfChangeAlreadyInQueue(change)
        if old_item:
            log = get_annotated_logger(self.log, event)
            log.debug("Change %s is a new version of %s, removing %s",
                      change, old_item.change, old_item)
            self.removeItem(old_item)

    def removeAbandonedChange(self, change, event):
        log = get_annotated_logger(self.log, event)
        log.debug("Change %s abandoned, removing." % change)
        for item in self.pipeline.getAllItems():
            if not item.live:
                continue
            if item.change.equals(change):
                self.removeItem(item)

    @abstractmethod
    def getChangeQueue(self, change, event, existing=None):
        pass

    def reEnqueueItem(self, item, last_head, old_item_ahead, item_ahead_valid):
        log = get_annotated_logger(self.log, item.event)
        with self.getChangeQueue(item.change, item.event,
                                 last_head.queue) as change_queue:
            if change_queue:
                log.debug("Re-enqueing change %s in queue %s",
                          item.change, change_queue)
                change_queue.enqueueItem(item)

                # If the old item ahead was re-enqued, this value will
                # be true, so we should attempt to move the item back
                # to where it was in case an item ahead is already
                # failing.
                if item_ahead_valid:
                    change_queue.moveItem(item, old_item_ahead)
                # Get an updated copy of the layout and update the job
                # graph if necessary.  This resumes the buildset merge
                # state machine.  If we have an up-to-date layout, it
                # will go ahead and refresh the job graph if needed;
                # or it will send a new merge job if necessary, or it
                # will do nothing if we're waiting on a merge job.
                has_job_graph = bool(item.job_graph)
                item.job_graph = None
                item.layout = None
                # If the item is no longer active, but has a job graph we
                # will make sure to update it.
                if item.active or has_job_graph:
                    self.prepareItem(item)

                # Re-set build results in case any new jobs have been
                # added to the tree.
                for build in item.current_build_set.getBuilds():
                    if build.result:
                        item.setResult(build)
                # Similarly, reset the item state.
                if item.current_build_set.unable_to_merge:
                    item.setUnableToMerge()
                if item.current_build_set.config_errors:
                    item.setConfigErrors(item.current_build_set.config_errors)
                if item.dequeued_needing_change:
                    item.setDequeuedNeedingChange()

                # It can happen that all in-flight builds have been removed
                # which would lead to paused parent jobs not being resumed.
                # To prevent that resume parent jobs if necessary.
                self._resumeBuilds(item.current_build_set)

                self.reportStats(item)
                return True
            else:
                log.error("Unable to find change queue for project %s",
                          item.change.project)
                return False

    def addChange(self, change, event, quiet=False, enqueue_time=None,
                  ignore_requirements=False, live=True,
                  change_queue=None, history=None, dependency_graph=None):
        log = get_annotated_logger(self.log, event)
        log.debug("Considering adding change %s" % change)

        history = history if history is not None else []
        log.debug("History: %s", history)

        # Ensure the dependency graph is created when the first change is
        # processed to allow cycle detection with the Tarjan algorithm
        dependency_graph = dependency_graph or collections.OrderedDict()
        log.debug("Dependency graph: %s", dependency_graph)

        # If we are adding a live change, check if it's a live item
        # anywhere in the pipeline.  Otherwise, we will perform the
        # duplicate check below on the specific change_queue.
        if live and self.isChangeAlreadyInPipeline(change):
            log.debug("Change %s is already in pipeline, ignoring" % change)
            return True

        if not ignore_requirements:
            for f in self.ref_filters:
                if f.connection_name != change.project.connection_name:
                    log.debug("Filter %s skipped for change %s due "
                              "to mismatched connections" % (f, change))
                    continue
                match_result = f.matches(change)
                if not match_result:
                    log.debug("Change %s does not match pipeline "
                              "requirement %s because %s" % (
                                  change, f, str(match_result)))
                    return False

        if not self.isChangeReadyToBeEnqueued(change, event):
            log.debug("Change %s is not ready to be enqueued, ignoring" %
                      change)
            return False

        with self.getChangeQueue(change, event, change_queue) as change_queue:
            if not change_queue:
                log.debug("Unable to find change queue for "
                          "change %s in project %s" %
                          (change, change.project))
                return False

            if not self.enqueueChangesAhead(change, event, quiet,
                                            ignore_requirements,
                                            change_queue, history=history,
                                            dependency_graph=dependency_graph):
                self.dequeueIncompleteCycle(change, dependency_graph, event,
                                            change_queue)
                log.debug("Failed to enqueue changes ahead of %s" % change)
                return False

            log.debug("History after enqueuing changes ahead: %s", history)

            if self.isChangeAlreadyInQueue(change, change_queue):
                log.debug("Change %s is already in queue, ignoring" % change)
                return True

            cycle = []
            if hasattr(change, "needs_changes"):
                cycle = self.cycleForChange(change, dependency_graph, event)
                if cycle and not self.canProcessCycle(change.project):
                    log.info("Dequeing change %s since at least one project "
                             "does not allow circular dependencies", change)
                    actions = self.pipeline.failure_actions
                    ci = model.QueueItem(self, cycle[-1], event)
                    ci.warning("Dependency cycle detected")
                    ci.setReportedResult('FAILURE')

                    # Only report the cycle if the project is in the current
                    # pipeline. Otherwise the change could be spammed by
                    # reports from unrelated pipelines.
                    if self.pipeline.tenant.layout.getProjectPipelineConfig(
                        ci
                    ):
                        self.sendReport(actions, ci)

                    return False

            log.info("Adding change %s to queue %s in %s" %
                     (change, change_queue, self.pipeline))
            item = change_queue.enqueueChange(change, event)
            self.updateBundle(item, change_queue, cycle)

            if enqueue_time:
                item.enqueue_time = enqueue_time
            item.live = live
            self.reportStats(item, added=True)
            item.quiet = quiet
            if item.live and not item.reported_enqueue:
                self.reportEnqueue(item)
                item.reported_enqueue = True

            # Items in a dependency cycle are expected to be enqueued after
            # each other. To prevent non-cycle items from being enqueued
            # between items of the same cycle, enqueue items behind each item
            # in the cycle once all items in the cycle are enqueued.
            if all([self.isChangeAlreadyInQueue(c, change_queue)
                    for c in cycle]):
                if cycle:
                    self.log.debug("Cycle complete, enqueing changes behind")
                for c in cycle or [change]:
                    self.enqueueChangesBehind(c, event, quiet,
                                              ignore_requirements,
                                              change_queue, history,
                                              dependency_graph)

            zuul_driver = self.sched.connections.drivers['zuul']
            tenant = self.pipeline.tenant
            zuul_driver.onChangeEnqueued(
                tenant, item.change, self.pipeline, event)
            self.dequeueSupercededItems(item)
            return True

    def cycleForChange(self, change, dependency_graph, event):
        log = get_annotated_logger(self.log, event)
        log.debug("Running Tarjan's algorithm on current dependencies: %s",
                  dependency_graph)
        sccs = [s for s in strongly_connected_components(dependency_graph)
                if len(s) > 1]
        log.debug("Strongly connected components (cyles): %s", sccs)
        for scc in sccs:
            if change in scc:
                log.debug("Dependency cycle detected for "
                          "change %s in project %s",
                          change, change.project)
                # Change can not be part of multiple cycles, so we can return
                return scc
        return []

    def canProcessCycle(self, project):
        layout = self.pipeline.tenant.layout
        pipeline_queue_name = None
        project_queue_name = None
        for project_config in layout.getAllProjectConfigs(
            project.canonical_name
        ):
            if not project_queue_name:
                project_queue_name = project_config.queue_name

            project_pipeline_config = project_config.pipelines.get(
                self.pipeline.name)

            if project_pipeline_config is None:
                continue

            # TODO(simonw): Remove pipeline_queue_name after deprecation
            if not pipeline_queue_name:
                pipeline_queue_name = project_pipeline_config.queue_name

        # Note: we currently support queue name per pipeline and per
        # project while project has precedence.
        queue_name = project_queue_name or pipeline_queue_name
        if queue_name is None:
            return False

        queue_config = layout.queues.get(queue_name)
        return (
            queue_config is not None and
            queue_config.allow_circular_dependencies
        )

    def canMergeCycle(self, bundle):
        """Check if the cycle still fulfills the pipeline's ready criteria."""
        return True

    def updateBundle(self, item, change_queue, cycle):
        if not cycle:
            return

        log = get_annotated_logger(self.log, item.event)
        item.bundle = model.Bundle()

        # Try to find already enqueued items of this cycle, so we use
        # the same bundle
        for needed_change in (c for c in cycle if c is not item.change):
            needed_item = self.getItemForChange(needed_change, change_queue)
            if not needed_item:
                continue
            # Use a common bundle for the cycle
            item.bundle = needed_item.bundle
            break

        log.info("Adding cycle item %s to bundle %s", item, item.bundle)
        item.bundle.add_item(item)

    def dequeueIncompleteCycle(self, change, dependency_graph, event,
                               change_queue):
        log = get_annotated_logger(self.log, event)
        cycle = self.cycleForChange(change, dependency_graph, event)
        enqueued_cycle_items = [i for i in (self.getItemForChange(c,
                                                                  change_queue)
                                            for c in cycle) if i is not None]
        if enqueued_cycle_items:
            log.info("Dequeuing incomplete cycle items: %s",
                     enqueued_cycle_items)
            for cycle_item in enqueued_cycle_items:
                self.dequeueItem(cycle_item)

    def dequeueItem(self, item):
        log = get_annotated_logger(self.log, item.event)
        log.debug("Removing change %s from queue", item.change)
        item.queue.dequeueItem(item)
        # In case a item is dequeued that doesn't have a result yet
        # (success/failed/...) we report it as dequeued.
        # Without this check, all items with a valid result would be reported
        # twice.
        if not item.current_build_set.result and item.live:
            self.reportDequeue(item)

    def removeItem(self, item):
        log = get_annotated_logger(self.log, item.event)
        # Remove an item from the queue, probably because it has been
        # superseded by another change.
        log.debug("Canceling builds behind change: %s "
                  "because it is being removed.", item.change)
        self.cancelJobs(item)
        self.dequeueItem(item)
        self.reportStats(item)

        if item.bundle is None:
            return

        log.debug("Dequeueing items in bundle %s", item.bundle)
        bundle_iter = (i for i in item.bundle.items if i is not item)
        for bundle_item in bundle_iter:
            self.cancelJobs(bundle_item)
            self.dequeueItem(bundle_item)
            self.reportStats(bundle_item)

    def dequeueSupercededItems(self, item):
        for other_name in self.pipeline.supercedes:
            other_pipeline = self.pipeline.tenant.layout.pipelines.get(
                other_name)
            if not other_pipeline:
                continue

            found = None
            for other_item in other_pipeline.getAllItems():
                if other_item.live and other_item.change.equals(item.change):
                    found = other_item
                    break
            if found:
                self.log.info("Item %s is superceded by %s, removing" %
                              (found, item))
                other_pipeline.manager.removeItem(found)

    def updateCommitDependencies(self, change, change_queue, event):
        log = get_annotated_logger(self.log, event)

        # Search for Depends-On headers and find appropriate changes
        log.debug("  Updating commit dependencies for %s", change)
        change.refresh_deps = False
        dependencies = []
        seen = set()
        for match in find_dependency_headers(change.message):
            log.debug("  Found Depends-On header: %s", match)
            if match in seen:
                continue
            seen.add(match)
            try:
                url = urllib.parse.urlparse(match)
            except ValueError:
                continue
            source = self.sched.connections.getSourceByHostname(
                url.hostname)
            if not source:
                continue
            log.debug("  Found source: %s", source)
            dep = source.getChangeByURL(match, event)
            if dep and (not dep.is_merged) and dep not in dependencies:
                log.debug("  Adding dependency: %s", dep)
                dependencies.append(dep)
        change.commit_needs_changes = dependencies

    def provisionNodes(self, item):
        log = item.annotateLogger(self.log)
        jobs = item.findJobsToRequest(item.pipeline.tenant.semaphore_handler)
        if not jobs:
            return False
        build_set = item.current_build_set
        log.debug("Requesting nodes for change %s", item.change)
        if self.sched.use_relative_priority:
            priority = item.getNodePriority()
        else:
            priority = 0
        for job in jobs:
            req = self.sched.nodepool.requestNodes(
                build_set, job, priority, event=item.event)
            log.debug("Adding node request %s for job %s to item %s",
                      req, job, item)
            build_set.setJobNodeRequest(job.name, req)
        return True

    def _executeJobs(self, item, jobs):
        log = get_annotated_logger(self.log, item.event)
        log.debug("Executing jobs for change %s", item.change)
        build_set = item.current_build_set
        for job in jobs:
            log.debug("Found job %s for change %s", job, item.change)
            try:
                nodeset = item.current_build_set.getJobNodeSet(job.name)
                self.sched.nodepool.useNodeSet(
                    nodeset, build_set=item.current_build_set,
                    event=item.event)
                self.sched.executor.execute(
                    job, item, self.pipeline,
                    build_set.dependent_changes,
                    build_set.merger_items)
            except Exception:
                log.exception("Exception while executing job %s "
                              "for change %s:", job, item.change)
                try:
                    # If we hit an exception we don't have a build in the
                    # current item so a potentially aquired semaphore must be
                    # released as it won't be released on dequeue of the item.
                    tenant = item.pipeline.tenant
                    tenant.semaphore_handler.release(item, job)
                except Exception:
                    log.exception("Exception while releasing semaphore")

    def executeJobs(self, item):
        # TODO(jeblair): This should return a value indicating a job
        # was executed.  Appears to be a longstanding bug.
        if not item.layout:
            return False

        jobs = item.findJobsToRun(
            item.pipeline.tenant.semaphore_handler)
        if jobs:
            self._executeJobs(item, jobs)

    def cancelJobs(self, item, prime=True):
        log = get_annotated_logger(self.log, item.event)
        log.debug("Cancel jobs for change %s", item.change)
        canceled = False
        old_build_set = item.current_build_set
        jobs_to_cancel = item.getJobs()

        # Don't reset builds for a failing bundle when it has already started
        # reporting, to keep available build results. Those items will be
        # reported immediately afterwards during queue processing.
        if (prime and item.current_build_set.ref and not
                item.didBundleStartReporting()):
            item.resetAllBuilds()

        for job in jobs_to_cancel:
            self.sched.cancelJob(old_build_set, job)

        for item_behind in item.items_behind:
            log.debug("Canceling jobs for change %s, behind change %s",
                      item_behind.change, item.change)
            if self.cancelJobs(item_behind, prime=prime):
                canceled = True
        return canceled

    def _findRelevantErrors(self, item, layout):
        if item.item_ahead:
            parent_layout = item.item_ahead.layout
        else:
            parent_layout = item.pipeline.tenant.layout

        relevant_errors = []
        for err in layout.loading_errors.errors:
            econtext = err.key.context
            if ((err.key not in
                 parent_layout.loading_errors.error_keys) or
                (econtext.project == item.change.project.name and
                 econtext.branch == item.change.branch)):
                relevant_errors.append(err)
        return relevant_errors

    def _loadDynamicLayout(self, item):
        log = get_annotated_logger(self.log, item.event)
        # Load layout
        # Late import to break an import loop
        import zuul.configloader
        loader = zuul.configloader.ConfigLoader(
            self.sched.connections, self.sched, None, None)

        log.debug("Loading dynamic layout")

        (trusted_updates, untrusted_updates) = item.includesConfigUpdates()
        build_set = item.current_build_set
        trusted_layout = None
        trusted_errors = False
        untrusted_layout = None
        untrusted_errors = False
        try:
            # First parse the config as it will land with the
            # full set of config and project repos.  This lets us
            # catch syntax errors in config repos even though we won't
            # actually run with that config.
            if trusted_updates:
                log.debug("Loading dynamic layout (phase 1)")
                trusted_layout = loader.createDynamicLayout(
                    item,
                    build_set.files,
                    self.sched.ansible_manager,
                    include_config_projects=True,
                    zuul_event_id=None)
                trusted_errors = len(trusted_layout.loading_errors) > 0

            # Then create the config a second time but without changes
            # to config repos so that we actually use this config.
            if untrusted_updates:
                log.debug("Loading dynamic layout (phase 2)")
                untrusted_layout = loader.createDynamicLayout(
                    item,
                    build_set.files,
                    self.sched.ansible_manager,
                    include_config_projects=False,
                    zuul_event_id=None)
                untrusted_errors = len(untrusted_layout.loading_errors) > 0

            # Configuration state handling switchboard. Intentionally verbose
            # and repetetive to be exceptionally clear that we handle all
            # possible cases correctly. Note we never return trusted_layout
            # from a dynamic update.

            # No errors found at all use dynamic untrusted layout
            if (trusted_layout and not trusted_errors and
                    untrusted_layout and not untrusted_errors):
                log.debug("Loading dynamic layout complete")
                return untrusted_layout
            # No errors in untrusted only layout update
            elif (not trusted_layout and
                    untrusted_layout and not untrusted_errors):
                log.debug("Loading dynamic layout complete")
                return untrusted_layout
            # No errors in trusted only layout update
            elif (not untrusted_layout and
                    trusted_layout and not trusted_errors):
                # We're a change to a config repo (with no untrusted
                # config items ahead), so just use the current pipeline
                # layout.
                log.debug("Loading dynamic layout complete")
                return item.queue.pipeline.tenant.layout
            # Untrusted layout only works with trusted updates
            elif (trusted_layout and not trusted_errors and
                    untrusted_layout and untrusted_errors):
                log.info("Configuration syntax error in dynamic layout")
                # The config is good if we include config-projects,
                # but is currently invalid if we omit them.  Instead
                # of returning the whole error message, just leave a
                # note that the config will work once the dependent
                # changes land.
                msg = "This change depends on a change "\
                      "to a config project.\n\n"
                msg += textwrap.fill(textwrap.dedent("""\
                The syntax of the configuration in this change has
                been verified to be correct once the config project
                change upon which it depends is merged, but it can not
                be used until that occurs."""))
                item.setConfigError(msg)
                return None
            # Untrusted layout is broken and trusted is broken or not set
            elif untrusted_layout and untrusted_errors:
                # Find a layout loading error that match
                # the current item.change and only report
                # if one is found.
                relevant_errors = self._findRelevantErrors(item,
                                                           untrusted_layout)
                if relevant_errors:
                    item.setConfigErrors(relevant_errors)
                    return None
                log.info(
                    "Configuration syntax error not related to "
                    "change context. Error won't be reported.")
                return untrusted_layout
            # Trusted layout is broken
            elif trusted_layout and trusted_errors:
                # Find a layout loading error that match
                # the current item.change and only report
                # if one is found.
                relevant_errors = self._findRelevantErrors(item,
                                                           trusted_layout)
                if relevant_errors:
                    item.setConfigErrors(relevant_errors)
                    return None
                log.info(
                    "Configuration syntax error not related to "
                    "change context. Error won't be reported.")
                # We're a change to a config repo with errors not relevant
                # to this repo. We use the pipeline layout.
                return item.queue.pipeline.tenant.layout
            else:
                raise Exception("We have reached a configuration error that is"
                                "not accounted for.")

        except Exception:
            log.exception("Error in dynamic layout")
            item.setConfigError("Unknown configuration error")
            return None

    def getLayout(self, item):
        if item.item_ahead:
            fallback_layout = item.item_ahead.layout
            if fallback_layout is None:
                # We're probably waiting on a merge job for the item ahead.
                return None
        else:
            fallback_layout = item.pipeline.tenant.layout

        # If the current change does not update the layout, use its parent.
        # If the bundle doesn't update the config or the bundle updates the
        # config but the current change's project is not part of the tenant
        # (e.g. when dealing w/ cross-tenant cycles), use the parent layout.
        if not (
            item.change.updatesConfig(item.pipeline.tenant) or
            (
                item.bundle
                and item.bundle.updatesConfig(item.pipeline.tenant)
                and item.pipeline.tenant.getProject(
                    item.change.project.canonical_name
                )[1] is not None
            )
        ):
            return fallback_layout
        # Else this item updates the config,
        # ask the merger for the result.
        build_set = item.current_build_set
        if build_set.merge_state != build_set.COMPLETE:
            return None
        if build_set.unable_to_merge:
            return fallback_layout
        self.log.debug("Preparing dynamic layout for: %s" % item.change)
        return self._loadDynamicLayout(item)

    def _branchesForRepoState(self, projects, tenant, items=None):
        if all(tenant.getExcludeUnprotectedBranches(project)
               for project in projects):
            branches = set()

            # Add all protected branches of all involved projects
            for project in projects:
                branches.update(tenant.getProjectBranches(project))

            # Additionally add all target branches of all involved items.
            if items is not None:
                branches.update(item.change.branch for item in items
                                if hasattr(item.change, 'branch'))
            branches = list(branches)
        else:
            branches = None
        return branches

    def scheduleMerge(self, item, files=None, dirs=None):
        log = item.annotateLogger(self.log)
        log.debug("Scheduling merge for item %s (files: %s, dirs: %s)" %
                  (item, files, dirs))
        build_set = item.current_build_set
        build_set.merge_state = build_set.PENDING

        # If the involved projects exclude unprotected branches we should also
        # exclude them from the merge and repo state except the branch of the
        # change that is tested.
        tenant = item.pipeline.tenant
        items = list(item.items_ahead) + [item]
        if item.bundle:
            items.extend(item.bundle.items)
        projects = {
            item.change.project for item in items
            if tenant.getProject(item.change.project.canonical_name)[1]
        }
        branches = self._branchesForRepoState(projects=projects, tenant=tenant,
                                              items=items)

        if isinstance(item.change, model.Change):
            self.sched.merger.mergeChanges(build_set.merger_items,
                                           item.current_build_set, files, dirs,
                                           precedence=self.pipeline.precedence,
                                           event=item.event,
                                           branches=branches)
        else:
            self.sched.merger.getRepoState(build_set.merger_items,
                                           item.current_build_set,
                                           precedence=self.pipeline.precedence,
                                           event=item.event,
                                           branches=branches)
        return False

    def scheduleFilesChanges(self, item):
        log = item.annotateLogger(self.log)
        log.debug("Scheduling fileschanged for item %s", item)
        build_set = item.current_build_set
        build_set.files_state = build_set.PENDING

        self.sched.merger.getFilesChanges(
            item.change.project.connection_name, item.change.project.name,
            item.change.ref, item.change.branch, build_set=build_set,
            event=item.event)
        return False

    def scheduleGlobalRepoState(self, item: QueueItem) -> bool:
        log = item.annotateLogger(self.log)
        log.info('Scheduling global repo state for item %s', item)

        tenant = item.pipeline.tenant
        jobs = item.job_graph.getJobs()
        projects = set()
        for job in jobs:
            log.debug('Processing job %s', job.name)
            projects.update(job.getAffectedProjects(tenant))
            log.debug('Needed projects: %s', projects)

        # Filter projects for ones that are already in repo state
        repo_state = item.current_build_set.repo_state
        connections = self.sched.connections.connections
        projects_to_remove = set()
        for connection in repo_state.keys():
            canonical_hostname = connections[connection].canonical_hostname
            for project in repo_state[connection].keys():
                canonical_project_name = canonical_hostname + '/' + project
                for affected_project in projects:
                    if canonical_project_name ==\
                            affected_project.canonical_name:
                        projects_to_remove.add(affected_project)
        projects -= projects_to_remove

        if not projects:
            item.current_build_set.repo_state_state =\
                item.current_build_set.COMPLETE
            return True

        branches = self._branchesForRepoState(projects=projects, tenant=tenant)

        new_items = list()
        for project in projects:
            new_item = dict()
            new_item['project'] = project.name
            new_item['connection'] = project.connection_name
            new_items.append(new_item)

        # Get state for not yet tracked projects
        self.sched.merger.getRepoState(items=new_items,
                                       build_set=item.current_build_set,
                                       event=item.event,
                                       branches=branches)
        return True

    def prepareItem(self, item: QueueItem) -> bool:
        build_set = item.current_build_set
        tenant = item.pipeline.tenant
        # We always need to set the configuration of the item if it
        # isn't already set.
        tpc = tenant.project_configs.get(item.change.project.canonical_name)
        if not build_set.ref:
            build_set.setConfiguration()

        # Next, if a change ahead has a broken config, then so does
        # this one.  Record that and don't do anything else.
        if (item.item_ahead and item.item_ahead.current_build_set and
            item.item_ahead.current_build_set.config_errors):
            msg = "This change depends on a change "\
                  "with an invalid configuration.\n"
            item.setConfigError(msg)
            return False

        # The next section starts between 0 and 2 remote merger
        # operations in parallel as needed.
        ready = True
        # If the project is in this tenant, fetch missing files so we
        # know if it updates the config.
        if tpc:
            if build_set.files_state == build_set.NEW:
                ready = self.scheduleFilesChanges(item)
            if build_set.files_state == build_set.PENDING:
                ready = False
        # If this change alters config or is live, schedule merge and
        # build a layout.
        # If we are dealing w/ a bundle and the bundle updates config we also
        # have to merge since a config change in any of the bundle's items
        # applies to all items. This is, unless the current item is not part
        # of this tenant (e.g. cross-tenant cycle).
        if build_set.merge_state == build_set.NEW:
            if item.live or item.change.updatesConfig(tenant) or (
                item.bundle and
                item.bundle.updatesConfig(tenant) and tpc is not None
            ):
                ready = self.scheduleMerge(
                    item,
                    files=(['zuul.yaml', '.zuul.yaml'] +
                           list(tpc.extra_config_files)),
                    dirs=(['zuul.d', '.zuul.d'] +
                          list(tpc.extra_config_dirs)))
        if build_set.merge_state == build_set.PENDING:
            ready = False

        # If a merger op is outstanding, we're not ready.
        if not ready:
            return False

        # With the merges done, we have the info needed to get a
        # layout.  This may return the pipeline layout, a layout from
        # a change ahead, a newly generated layout for this change, or
        # None if there was an error that makes the layout unusable.
        # In the last case, it will have set the config_errors on this
        # item, which may be picked up by the next itme.
        if not item.layout:
            item.layout = self.getLayout(item)
        if not item.layout:
            return False

        # If the change can not be merged or has config errors, don't
        # run jobs.
        if build_set.unable_to_merge:
            return False
        if build_set.config_errors:
            return False

        # We don't need to build a job graph for a non-live item, we
        # just need the layout.
        if not item.live:
            return False

        # At this point we have a layout for the item, and it's live,
        # so freeze the job graph.
        log = item.annotateLogger(self.log)
        if not item.job_graph:
            try:
                log.debug("Freezing job graph for %s" % (item,))
                item.freezeJobGraph()
            except Exception as e:
                # TODOv3(jeblair): nicify this exception as it will be reported
                log.exception("Error freezing job graph for %s" % (item,))
                item.setConfigError("Unable to freeze job graph: %s" %
                                    (str(e)))
                return False

        # At this point we know all frozen jobs and their repos so update the
        # repo state with all missing repos.
        if build_set.repo_state_state == build_set.NEW:
            build_set.repo_state_state = build_set.PENDING
            self.scheduleGlobalRepoState(item)
        if build_set.repo_state_state == build_set.PENDING:
            return False

        return True

    def _processOneItem(self, item, nnfi):
        log = item.annotateLogger(self.log)
        changed = False
        ready = False
        dequeued = False
        failing_reasons = []  # Reasons this item is failing

        item_ahead = item.item_ahead
        if item_ahead and (not item_ahead.live):
            item_ahead = None
        change_queue = item.queue

        if self.checkForChangesNeededBy(item.change, change_queue,
                                        item.event) is not True:
            # It's not okay to enqueue this change, we should remove it.
            log.info("Dequeuing change %s because "
                     "it can no longer merge" % item.change)
            self.cancelJobs(item)
            self.dequeueItem(item)
            if item.isBundleFailing():
                item.setDequeuedBundleFailing()
            else:
                item.setDequeuedNeedingChange()
            if item.live:
                try:
                    self.reportItem(item)
                except exceptions.MergeFailure:
                    pass
            return (True, nnfi)

        actionable = change_queue.isActionable(item)
        item.active = actionable

        dep_items = self.getFailingDependentItems(item)
        if dep_items:
            failing_reasons.append('a needed change is failing')
            self.cancelJobs(item, prime=False)
        else:
            item_ahead_merged = False
            if (item_ahead and
                hasattr(item_ahead.change, 'is_merged') and
                item_ahead.change.is_merged):
                item_ahead_merged = True
            if (item_ahead != nnfi and not item_ahead_merged):
                # Our current base is different than what we expected,
                # and it's not because our current base merged.  Something
                # ahead must have failed.
                log.info("Resetting builds for change %s because the "
                         "item ahead, %s, is not the nearest non-failing "
                         "item, %s" % (item.change, item_ahead, nnfi))
                change_queue.moveItem(item, nnfi)
                changed = True
                self.cancelJobs(item)
            if actionable:
                ready = self.prepareItem(item)
                # Starting jobs reporting should only be done once if there are
                # jobs to run for this item.
                if ready and len(self.pipeline.start_actions) > 0 \
                        and len(item.job_graph.jobs) > 0 \
                        and not item.reported_start \
                        and not item.quiet:
                    self.reportStart(item)
                    item.reported_start = True
                if item.current_build_set.unable_to_merge:
                    failing_reasons.append("it has a merge conflict")
                if item.current_build_set.config_errors:
                    failing_reasons.append("it has an invalid configuration")
                if ready and self.provisionNodes(item):
                    changed = True
                if ready and item.bundle and item.didBundleFinish():
                    # Since the bundle finished we need to check if any item
                    # can report. If that's the case we need to process the
                    # queue again.
                    changed = changed or any(
                        i.item_ahead is None for i in item.bundle.items)
        if ready and self.executeJobs(item):
            changed = True

        if item.hasAnyJobFailed():
            failing_reasons.append("at least one job failed")
        if (not item.live) and (not item.items_behind) and (not dequeued):
            failing_reasons.append("is a non-live item with no items behind")
            self.dequeueItem(item)
            changed = dequeued = True

        can_report = not item_ahead and item.areAllJobsComplete() and item.live
        if can_report and item.bundle:
            can_report = can_report and (
                item.isBundleFailing() or item.didBundleFinish()
            )
            # Before starting to merge the cycle items, make sure they
            # can still be merged, to reduce the chance of a partial merge.
            if (
                can_report
                and not item.bundle.started_reporting
                and not self.canMergeCycle(item.bundle)
            ):
                item.bundle.cannot_merge = True
                failing_reasons.append("cycle can not be merged")
                log.debug(
                    "Dequeuing item %s because cycle can no longer merge",
                    item
                )
            item.bundle.started_reporting = can_report

        if can_report:
            try:
                self.reportItem(item)
            except exceptions.MergeFailure:
                failing_reasons.append("it did not merge")
                for item_behind in item.items_behind:
                    log.info("Resetting builds for change %s because the "
                             "item ahead, %s, failed to merge" %
                             (item_behind.change, item))
                    self.cancelJobs(item_behind)
                # Only re-reported items in the cycle when we encounter a merge
                # failure for a successful bundle.
                if (item.bundle and not (
                        item.isBundleFailing() or item.cannotMergeBundle())):
                    item.bundle.failed_reporting = True
                    self.reportProcessedBundleItems(item)
            self.dequeueItem(item)
            changed = dequeued = True
        elif not failing_reasons and item.live:
            nnfi = item
        item.current_build_set.failing_reasons = failing_reasons
        if failing_reasons:
            log.debug("%s is a failing item because %s" %
                      (item, failing_reasons))
        if item.live and not dequeued and self.sched.use_relative_priority:
            priority = item.getNodePriority()
            for node_request in item.current_build_set.node_requests.values():
                if node_request.relative_priority != priority:
                    self.sched.nodepool.reviseRequest(
                        node_request, priority)
        return (changed, nnfi)

    def reportProcessedBundleItems(self, item):
        """Report failure to already reported bundle items.

        In case we encounter e.g. a merge failure when we already successfully
        reported some items, we need to go back and report again.
        """
        reported_items = [i for i in item.bundle.items if i.reported]

        actions = self.pipeline.failure_actions
        for ri in reported_items:
            ri.setReportedResult('FAILURE')
            self.sendReport(actions, ri)

    def processQueue(self):
        # Do whatever needs to be done for each change in the queue
        self.log.debug("Starting queue processor: %s" % self.pipeline.name)
        changed = False
        for queue in self.pipeline.queues:
            queue_changed = False
            nnfi = None  # Nearest non-failing item
            for item in queue.queue[:]:
                item_changed, nnfi = self._processOneItem(
                    item, nnfi)
                if item_changed:
                    queue_changed = True
                self.reportStats(item)
            if queue_changed:
                changed = True
                status = ''
                for item in queue.queue:
                    status += item.formatStatus()
                if status:
                    self.log.debug("Queue %s status is now:\n %s" %
                                   (queue.name, status))
        self.log.debug("Finished queue processor: %s (changed: %s)" %
                       (self.pipeline.name, changed))
        return changed

    def onBuildStarted(self, build):
        log = get_annotated_logger(self.log, build.zuul_event_id)
        log.debug("Build %s started", build)
        return True

    def onBuildPaused(self, build):
        log = get_annotated_logger(self.log, build.zuul_event_id)
        item = build.build_set.item
        log.debug("Build %s of %s paused", build, item.change)
        item.setResult(build)

        # We need to resume builds because we could either have no children
        # or have children that are already skipped.
        self._resumeBuilds(build.build_set)
        return True

    def _resumeBuilds(self, build_set):
        """
        Resumes all paused builds of a buildset that may be resumed.
        """
        jobgraph = build_set.item.job_graph
        for build in build_set.builds.values():
            if not build.paused:
                continue
            # check if all child jobs are finished
            child_builds = [build_set.builds.get(x.name) for x in
                            jobgraph.getDependentJobsRecursively(
                                build.job.name)]
            all_completed = True
            for child_build in child_builds:
                if not child_build or not child_build.result:
                    all_completed = False
                    break

            if all_completed:
                self.sched.executor.resumeBuild(build)
                build.paused = False

    def _resetDependentBuilds(self, build_set, build):
        jobgraph = build_set.item.job_graph

        for job in jobgraph.getDependentJobsRecursively(build.job.name):
            self.sched.cancelJob(build_set, job)
            build = build_set.getBuild(job.name)
            if build:
                build_set.removeBuild(build)

        # Re-set build results in case we resetted builds that were skipped
        # not by this build/
        for build in build_set.getBuilds():
            if build.result:
                build_set.item.setResult(build)

    def _cancelRunningBuilds(self, build_set):
        item = build_set.item
        for job in item.getJobs():
            build = build_set.getBuild(job.name)
            if not build or not build.result:
                self.sched.cancelJob(build_set, job, final=True)

    def onBuildCompleted(self, build):
        log = get_annotated_logger(self.log, build.zuul_event_id)
        item = build.build_set.item

        log.debug("Build %s of %s completed" % (build, item.change))
        item.pipeline.tenant.semaphore_handler.release(item, build.job)

        if item.getJob(build.job.name) is None:
            log.info("Build %s no longer in job graph for item %s",
                     build, item)
            return

        item.setResult(build)
        log.debug("Item %s status is now:\n %s", item, item.formatStatus())

        if build.retry:
            if build.build_set.getJobNodeSet(build.job.name):
                build.build_set.removeJobNodeSet(build.job.name)

            # in case this was a paused build we need to retry all child jobs
            self._resetDependentBuilds(build.build_set, build)

        self._resumeBuilds(build.build_set)

        if (item.project_pipeline_config.fail_fast and
            build.failed and build.job.voting and not build.retry):
            # If fail-fast is set and the build is not successful
            # cancel all remaining jobs.
            log.debug("Build %s failed and fail-fast enabled, canceling "
                      "running builds", build)
            self._cancelRunningBuilds(build.build_set)

        return True

    def onFilesChangesCompleted(self, event):
        build_set = event.build_set
        item = build_set.item
        item.change.files = event.files
        build_set.files_state = build_set.COMPLETE

    def onMergeCompleted(self, event):
        build_set = event.build_set
        if build_set.merge_state == build_set.COMPLETE:
            self._onGlobalRepoStateCompleted(event)
        else:
            self._onMergeCompleted(event)

    def _onMergeCompleted(self, event):
        build_set = event.build_set
        item = build_set.item
        item.change.containing_branches = event.item_in_branches
        build_set.merge_state = build_set.COMPLETE
        build_set.repo_state = event.repo_state
        if event.merged:
            build_set.commit = event.commit
            items_ahead = item.getNonLiveItemsAhead()
            for index, item in enumerate(items_ahead):
                files = item.current_build_set.files
                files.setFiles(event.files[:index + 1])
            build_set.files.setFiles(event.files)
        elif event.updated:
            build_set.commit = (item.change.newrev or
                                '0000000000000000000000000000000000000000')
        if not build_set.commit:
            self.log.info("Unable to merge change %s" % item.change)
            item.setUnableToMerge()

    def _onGlobalRepoStateCompleted(self, event):
        if not event.updated:
            item = event.build_set.item
            self.log.info("Unable to get global repo state for change %s"
                          % item.change)
            item.setUnableToMerge()
        else:
            repo_state = event.build_set.repo_state
            for connection in event.repo_state.keys():
                if connection in repo_state:
                    repo_state[connection].update(event.repo_state[connection])
                else:
                    repo_state[connection] = event.repo_state[connection]
            event.build_set.repo_state_state = event.build_set.COMPLETE

    def onNodesProvisioned(self, event):
        # TODOv3(jeblair): handle provisioning failure here
        request = event.request
        log = get_annotated_logger(self.log, request.event_id)

        build_set = request.build_set
        build_set.jobNodeRequestComplete(request.job.name,
                                         request.nodeset)
        if request.failed or not request.fulfilled:
            log.info("Node request %s: failure for %s",
                     request, request.job.name)
            build_set.item.setNodeRequestFailure(request.job)
            self._resumeBuilds(request.build_set)
            tenant = build_set.item.pipeline.tenant
            tenant.semaphore_handler.release(build_set.item, request.job)

        log.info("Completed node request %s for job %s of item %s "
                 "with nodes %s",
                 request, request.job, build_set.item, request.nodeset)

    def reportItem(self, item):
        log = get_annotated_logger(self.log, item.event)
        if not item.reported:
            # _reportItem() returns True if it failed to report.
            item.reported = not self._reportItem(item)
        if self.changes_merge:
            succeeded = item.didAllJobsSucceed() and not item.isBundleFailing()
            merged = item.reported
            source = item.change.project.source
            if merged:
                merged = source.isMerged(item.change, item.change.branch)
            change_queue = item.queue
            if not (succeeded and merged):
                if not item.job_graph or not item.job_graph.jobs:
                    error_reason = "did not have any jobs configured"
                elif not succeeded:
                    error_reason = "failed tests"
                else:
                    error_reason = "failed to merge"
                log.info("Reported change %s did not merge because it %s,"
                         "status: all-succeeded: %s, merged: %s",
                         item.change, error_reason, succeeded, merged)
                if not succeeded:
                    change_queue.decreaseWindowSize()
                    log.debug("%s window size decreased to %s",
                              change_queue, change_queue.window)
                raise exceptions.MergeFailure(
                    "Change %s failed to merge" % item.change)
            else:
                log.info("Reported change %s status: all-succeeded: %s, "
                         "merged: %s", item.change, succeeded, merged)
                change_queue.increaseWindowSize()
                log.debug("%s window size increased to %s",
                          change_queue, change_queue.window)

                zuul_driver = self.sched.connections.drivers['zuul']
                tenant = self.pipeline.tenant
                zuul_driver.onChangeMerged(tenant, item.change, source)

    def _reportItem(self, item):
        log = get_annotated_logger(self.log, item.event)
        log.debug("Reporting change %s", item.change)
        ret = True  # Means error as returned by trigger.report

        # In the case of failure, we may not hove completed an initial
        # merge which would get the layout for this item, so in order
        # to determine whether this item's project is in this
        # pipeline, use the dynamic layout if available, otherwise,
        # fall back to the current static layout as a best
        # approximation.
        layout = (item.layout or self.pipeline.tenant.layout)

        project_in_pipeline = True
        ppc = None
        try:
            ppc = layout.getProjectPipelineConfig(item)
        except Exception:
            log.exception("Invalid config for change %s", item.change)
        if not ppc:
            log.debug("Project %s not in pipeline %s for change %s",
                      item.change.project, self.pipeline, item.change)
            project_in_pipeline = False
            actions = self.pipeline.no_jobs_actions
            item.setReportedResult('NO_JOBS')
        elif item.getConfigErrors():
            log.debug("Invalid config for change %s", item.change)
            # TODOv3(jeblair): consider a new reporter action for this
            actions = self.pipeline.merge_failure_actions
            item.setReportedResult('CONFIG_ERROR')
        elif item.didMergerFail():
            log.debug("Merger failure")
            actions = self.pipeline.merge_failure_actions
            item.setReportedResult('MERGER_FAILURE')
        elif item.wasDequeuedNeedingChange():
            log.debug("Dequeued needing change")
            actions = self.pipeline.failure_actions
            item.setReportedResult('FAILURE')
        elif not item.getJobs():
            # We don't send empty reports with +1
            log.debug("No jobs for change %s", item.change)
            actions = self.pipeline.no_jobs_actions
            item.setReportedResult('NO_JOBS')
        elif item.cannotMergeBundle():
            log.debug("Bundle can not be merged")
            actions = self.pipeline.failure_actions
            item.setReportedResult("FAILURE")
        elif item.isBundleFailing():
            log.debug("Bundle is failing")
            actions = self.pipeline.failure_actions
            item.setReportedResult("FAILURE")
            if not item.didAllJobsSucceed():
                self.pipeline._consecutive_failures += 1
        elif item.didAllJobsSucceed() and not item.isBundleFailing():
            log.debug("success %s", self.pipeline.success_actions)
            actions = self.pipeline.success_actions
            item.setReportedResult('SUCCESS')
            self.pipeline._consecutive_failures = 0
        else:
            actions = self.pipeline.failure_actions
            item.setReportedResult('FAILURE')
            self.pipeline._consecutive_failures += 1
        if project_in_pipeline and self.pipeline._disabled:
            actions = self.pipeline.disabled_actions
        # Check here if we should disable so that we only use the disabled
        # reporters /after/ the last disable_at failure is still reported as
        # normal.
        if (self.pipeline.disable_at and not self.pipeline._disabled and
            self.pipeline._consecutive_failures >= self.pipeline.disable_at):
            self.pipeline._disabled = True
        if actions:
            log.info("Reporting item %s, actions: %s", item, actions)
            ret = self.sendReport(actions, item)
            if ret:
                log.error("Reporting item %s received: %s", item, ret)
        return ret

    def reportStats(self, item, added=False):
        if not self.sched.statsd:
            return
        try:
            # Update the gauge on enqueue and dequeue, but timers only
            # when dequeing.
            if item.dequeue_time:
                dt = int((item.dequeue_time - item.enqueue_time) * 1000)
            else:
                dt = None
            items = len(self.pipeline.getAllItems())

            tenant = self.pipeline.tenant
            basekey = 'zuul.tenant.%s' % tenant.name
            key = '%s.pipeline.%s' % (basekey, self.pipeline.name)
            # stats.timers.zuul.tenant.<tenant>.pipeline.<pipeline>.resident_time
            # stats_counts.zuul.tenant.<tenant>.pipeline.<pipeline>.total_changes
            # stats.gauges.zuul.tenant.<tenant>.pipeline.<pipeline>.current_changes
            self.sched.statsd.gauge(key + '.current_changes', items)
            if dt:
                self.sched.statsd.timing(key + '.resident_time', dt)
                self.sched.statsd.incr(key + '.total_changes')
            if hasattr(item.change, 'branch'):
                hostname = (item.change.project.canonical_hostname.
                            replace('.', '_'))
                projectname = (item.change.project.name.
                               replace('.', '_').replace('/', '.'))
                projectname = projectname.replace('.', '_').replace('/', '.')
                branchname = item.change.branch.replace('.', '_').replace(
                    '/', '.')
                # stats.timers.zuul.tenant.<tenant>.pipeline.<pipeline>.
                #   project.<host>.<project>.<branch>.resident_time
                # stats_counts.zuul.tenant.<tenant>.pipeline.<pipeline>.
                #   project.<host>.<project>.<branch>.total_changes
                key += '.project.%s.%s.%s' % (hostname, projectname,
                                              branchname)
                if dt:
                    self.sched.statsd.timing(key + '.resident_time', dt)
                    self.sched.statsd.incr(key + '.total_changes')
            if added and hasattr(item.event, 'arrived_at_scheduler_timestamp'):
                now = time.time()
                arrived = item.event.arrived_at_scheduler_timestamp
                processing = int((now - arrived) * 1000)
                elapsed = int((now - item.event.timestamp) * 1000)
                self.sched.statsd.timing(
                    basekey + '.event_enqueue_processing_time',
                    processing)
                self.sched.statsd.timing(
                    basekey + '.event_enqueue_time', elapsed)
        except Exception:
            self.log.exception("Exception reporting pipeline stats")
