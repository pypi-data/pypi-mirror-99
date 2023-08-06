:title: Github Checks API

Github Checks API
=================

Github provides two distinct methods for reporting results; a "checks"
and a "status" API.

The `checks API`_ provides some additional features compared to the
`status API`_ like file comments and custom actions (e.g. cancel a
running build).

Either can be chosen when configuring Zuul to report for your Github
project.  However, there are some considerations to take into account
when choosing the API.

Design decisions
----------------

The Github checks API defines the concepts of `Check Suites`_ and
`Check Runs`_.  *Check suites* are a collection of *check runs* for a
specific commit and summarize a final status

A priori the check suite appears to be a good mapping for a pipeline
execution in Zuul, where a check run maps to a single job execution
that is part of the pipeline run.  Unfortunately, there are a few
problematic restrictions mapping between Github and Zuul concepts.

Github check suites are opaque and the current status, duration and
the overall conclusion are all calculated and set automatically
whenever an included check run is updated.  Most importantly, there
can only be one check suite per commit SHA, per app.  Thus there is no
facility for for Zuul to create multiple check suite results for a
change, e.g. one check suite for each pipeline such as check and gate.

The Github check suite thus does not map well to Zuul's concept of
multiple pipelines for a single change.  Since a check suite is unique
and global for the change, it can not be used to flag the status of
arbitrary pipelines.  This makes the check suite API insufficient for
recording details that Zuul needs such as "the check pipeline has
passed but the gate pipeline has failed".

Another issue is that Zuul only reports on the results of the whole
pipeline, not individual jobs.  Reporting each Zuul job as a separate
check is problematic for a number of reasons.

Zuul often runs the same job for the same change multiple times; for
example in the check and gate pipeline.  There is no facility for
these runs to be reported differently in the single check suite for
the Github change.

When configuring branch protection in Github, only a *check run* can
be selected as required status check.  This is in conflict with
managing jobs in pipelines with Zuul.  For example, to implement
branch protection on GitHub would mean listing each job as a dedicated
check, leading to a check run list that is not kept in sync with the
project's Zuul pipeline configuration.  Additionally, you loose some
of Zuul's features like non-voting jobs as Github branch protections
has no concept of a non-voting job.

Thus Zuul can integrate with the checks API, but only at a pipeline
level.  Each pipeline execution will map to a check-run result
reported to Github.

Behaviour in Zuul
-----------------

Reporting
~~~~~~~~~

The Github reporter is able to report both a status
:attr:`pipeline.<reporter>.<github source>.status` or a check
:attr:`pipeline.<reporter>.<github source>.check`. While it's possible to
configure a Github reporter to report both, it's recommended to use only one.
Reporting both might result in duplicated status check entries in the Github
PR (the section below the comments).

Trigger
~~~~~~~

The Github driver is able to trigger on a reported check
(:value:`pipeline.trigger.<github source>.event.check_run`) similar to a
reported status (:value:`pipeline.trigger.<github source>.action.status`).

Requirements
~~~~~~~~~~~~

While trigger and reporter differentiates between status and check, the Github
driver does not differentiate between them when it comes to pipeline
requirements. This is mainly because Github also doesn't differentiate between
both in terms of branch protection and `status checks`_.

Actions / Events
----------------

Github provides a set of default actions for check suites and check runs.
Those actions are available as buttons in the Github UI. Clicking on those
buttons will emit webhook events which will be handled by Zuul.

These actions are only available on failed check runs / check suites. So
far, a running or successful check suite / check run does not provide any
action from Github side.

Available actions are:

Re-run all checks
  Github emits a webhook event with type ``check_suite`` and action
  ``rerequested`` that is meant to re-run all check-runs contained in this
  check suite. Github does not provide the list of check-runs in that case,
  so it's up to the Github app what should run.

Re-run failed checks
  Github emits a webhook event with type ``check_run`` and action
  ``rerequested`` for each failed check run contained in this suite.

Re-run
  Github emits a webhook event with type ``check_run`` and action
  ``rerequested`` for the specific check run.

Zuul will handle all events except for the `Re-run all checks` event;
it does not make sense in the Zuul model to trigger all pipelines to
run simultaneously.

These events are unable to be customized in Github.  Github will
always report "You have successfully requested ..." despite nothing
listening to the event.  Therefore, it might be a solution to handle
the `Re-run all checks` event in Zuul similar to `Re-run failed
checks` just to not do anything while Github makes the user believe an
action was really triggered.


File comments (annotations)
---------------------------

Check runs can be used to post file comments directly in the files of the PR.
Those are similar to user comments, but must provide some more information.

Zuul jobs can already return file comments via ``zuul_return``
(see: :ref:`return_values`). We can simply use this return value, build the
necessary annotations (how Github calls it) from it and attach them to the
check run.


Custom actions
~~~~~~~~~~~~~~

Check runs can provide some custom actions which will result in additional
buttons being available in the Github UI for this specific check run.
Clicking on such a button will emit a webhook event with type ``check_run``
and action ``requested_action`` and will additionally contain the id/name of
the requested action which we can define when creating the action on the
check run.

We could use these custom actions to provide some "Re-run" action on a
running check run (which might otherwise be stuck in case a check run update
fails) or to abort a check run directly from the Github UI.


Restrictions and Recommendations
--------------------------------

Although both the checks API and the status API can be activated for a
Github reporter at the same time, it's not recommended to do so as this might
result in multiple status checks to be reported to the PR for the same pipeline
execution (which would result in duplicated entries in the status section below
the comments of a PR).

In case the update on a check run fails (e.g. request timeout when reporting
success or failure to Github), the check run will stay in status "in_progess"
and there will be no way to re-run the check run via the Github UI as the
predefined actions are only available on failed check runs.
Thus, it's recommended to configure a
:value:`pipeline.trigger.<github source>.action.comment` trigger on the
pipeline to still be able to trigger re-run of the stuck check run via e.g.
"recheck".

The check suite will only list check runs that were reported by Zuul. If
the requirements for a certain pipeline are not met and it is not run, the
check run for this pipeline won't be listed in the check suite. However,
this does not affect the required status checks. If the check run is enabled
as required, Github will still show it in the list of required status checks
- even if it didn't run yet - just not in the check suite.


.. _checks API: https://docs.github.com/v3/checks/
.. _status API: https://docs.github.com/v3/repos/statuses/
.. _Check Suites: https://docs.github.com/v3/checks/suites/
.. _Check Runs: https://docs.github.com/v3/checks/runs/
.. _status checks: https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/about-status-checks#types-of-status-checks-on-github
