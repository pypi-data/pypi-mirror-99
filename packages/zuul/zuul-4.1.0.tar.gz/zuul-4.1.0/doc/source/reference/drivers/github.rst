:title: GitHub Driver

.. _github_driver:

GitHub
======

The GitHub driver supports sources, triggers, and reporters.  It can
interact with the public GitHub service as well as site-local
installations of GitHub enterprise.

Configure GitHub
----------------

There are two options currently available. GitHub's project owner can either
manually setup web-hook or install a GitHub Application. In the first case,
the project's owner needs to know the zuul endpoint and the webhook secrets.


Web-Hook
........

To configure a project's `webhook events
<https://developer.github.com/webhooks/creating/>`_:

* Set *Payload URL* to
  ``http://<zuul-hostname>:<port>/api/connection/<connection-name>/payload``.

* Set *Content Type* to ``application/json``.

Select *Events* you are interested in. See below for the supported events.

You will also need to have a GitHub user created for your zuul:

* Zuul public key needs to be added to the GitHub account

* A api_token needs to be created too, see this `article
  <https://help.github.com/articles/creating-an-access-token-for-command-line-use/>`_

Then in the zuul.conf, set webhook_token and api_token.

Application
...........

.. NOTE Duplicate content here and in zuul-from-scratch.rst.  Keep them
   in sync.

To create a `GitHub application
<https://developer.github.com/apps/building-integrations/setting-up-and-registering-github-apps/registering-github-apps/>`_:

* Go to your organization settings page to create the application, e.g.:
  https://github.com/organizations/my-org/settings/apps/new
* Set GitHub App name to "my-org-zuul"
* Set Setup URL to your setup documentation, when user install the application
  they are redirected to this url
* Set Webhook URL to
  ``http://<zuul-hostname>:<port>/api/connection/<connection-name>/payload``.
* Create a Webhook secret
* Set permissions:

  * Repository administration: Read
  * Checks: Read & Write
  * Repository contents: Read & Write (write to let zuul merge change)
  * Issues: Read & Write
  * Pull requests: Read & Write
  * Commit statuses: Read & Write

* Set events subscription:

  * Check run
  * Commit comment
  * Create
  * Push
  * Release
  * Issue comment
  * Issues
  * Label
  * Pull request
  * Pull request review
  * Pull request review comment
  * Status

* Set Where can this GitHub App be installed to "Any account"
* Create the App
* Generate a Private key in the app settings page

Then in the zuul.conf, set webhook_token, app_id and app_key.
After restarting zuul-scheduler, verify in the 'Advanced' tab that the
Ping payload works (green tick and 200 response)

Users can now install the application using its public page, e.g.:
https://github.com/apps/my-org-zuul

.. note::
   GitHub Pull Requests that modify GitHub Actions workflow configuration
   files cannot be merged by application credentials (this is any Pull Request
   that edits the .github/workflows directory and its contents). These Pull
   Requests must be merged by a normal user account. This means that Zuul
   will be limited to posting test results and cannot merge these PRs
   automatically when they pass testing.

   GitHub Actions are still in Beta and this behavior may change.


Connection Configuration
------------------------

There are two forms of operation. Either the Zuul installation can be
configured as a `Github App`_ or it can be configured as a Webhook.

If the `Github App`_ approach is taken, the config settings ``app_id`` and
``app_key`` are required. If the Webhook approach is taken, the ``api_token``
setting is required.

The supported options in ``zuul.conf`` connections are:

.. attr:: <github connection>

   .. attr:: driver
      :required:

      .. value:: github

         The connection must set ``driver=github`` for GitHub connections.

   .. attr:: app_id

      App ID if you are using a *GitHub App*. Can be found under the
      **Public Link** on the right hand side labeled **ID**.

   .. attr:: app_key

      Path to a file containing the secret key Zuul will use to create
      tokens for the API interactions. In Github this is known as
      **Private key** and must be collected when generated.

   .. attr:: api_token

      API token for accessing GitHub if Zuul is configured with
      Webhooks.  See `Creating an access token for command-line use
      <https://help.github.com/articles/creating-an-access-token-for-command-line-use/>`_.

   .. attr:: webhook_token

      Required token for validating the webhook event payloads.  In
      the GitHub App Configuration page, this is called **Webhook
      secret**.  See `Securing your webhooks
      <https://developer.github.com/webhooks/securing/>`_.

   .. attr:: sshkey
      :default: ~/.ssh/id_rsa

      Path to SSH key to use when cloning github repositories if Zuul
      is configured with Webhooks.

   .. attr:: server
      :default: github.com

      Hostname of the github install (such as a GitHub Enterprise).

   .. attr:: canonical_hostname

      The canonical hostname associated with the git repos on the
      GitHub server.  Defaults to the value of :attr:`<github
      connection>.server`.  This is used to identify projects from
      this connection by name and in preparing repos on the filesystem
      for use by jobs.  Note that Zuul will still only communicate
      with the GitHub server identified by **server**; this option is
      useful if users customarily use a different hostname to clone or
      pull git repos so that when Zuul places them in the job's
      working directory, they appear under this directory name.

   .. attr:: verify_ssl
      :default: true

      Enable or disable ssl verification for GitHub Enterprise.  This
      is useful for a connection to a test installation.

   .. attr:: rate_limit_logging
      :default: true

      Enable or disable GitHub rate limit logging. If rate limiting is disabled
      in GitHub Enterprise this can save some network round trip times.

Trigger Configuration
---------------------
GitHub webhook events can be configured as triggers.

A connection name with the GitHub driver can take multiple events with
the following options.

.. attr:: pipeline.trigger.<github source>

   The dictionary passed to the GitHub pipeline ``trigger`` attribute
   supports the following attributes:

   .. attr:: event
      :required:

      The event from github. Supported events are:

      .. value:: pull_request

      .. value:: pull_request_review

      .. value:: push

      .. value:: check_run

   .. attr:: action

      A :value:`pipeline.trigger.<github source>.event.pull_request`
      event will have associated action(s) to trigger from. The
      supported actions are:

      .. value:: opened

         Pull request opened.

      .. value:: changed

         Pull request synchronized.

      .. value:: closed

         Pull request closed.

      .. value:: reopened

         Pull request reopened.

      .. value:: comment

         Comment added to pull request.

      .. value:: labeled

         Label added to pull request.

      .. value:: unlabeled

         Label removed from pull request.

      .. value:: status

         Status set on commit. The syntax is ``user:status:value``.
         This also can be a regular expression.

      A :value:`pipeline.trigger.<github
      source>.event.pull_request_review` event will have associated
      action(s) to trigger from. The supported actions are:

      .. value:: submitted

         Pull request review added.

      .. value:: dismissed

         Pull request review removed.

      A :value:`pipeline.trigger.<github source>.event.check_run`
      event will have associated action(s) to trigger from. The
      supported actions are:

      .. value:: requested

         A check run is requested.

      .. value:: completed

         A check run completed.

   .. attr:: branch

      The branch associated with the event. Example: ``master``.  This
      field is treated as a regular expression, and multiple branches
      may be listed. Used for ``pull_request`` and
      ``pull_request_review`` events.

   .. attr:: comment

      This is only used for ``pull_request`` ``comment`` actions.  It
      accepts a list of regexes that are searched for in the comment
      string. If any of these regexes matches a portion of the comment
      string the trigger is matched.  ``comment: retrigger`` will
      match when comments containing 'retrigger' somewhere in the
      comment text are added to a pull request.

   .. attr:: label

      This is only used for ``labeled`` and ``unlabeled``
      ``pull_request`` actions.  It accepts a list of strings each of
      which matches the label name in the event literally.  ``label:
      recheck`` will match a ``labeled`` action when pull request is
      labeled with a ``recheck`` label. ``label: 'do not test'`` will
      match a ``unlabeled`` action when a label with name ``do not
      test`` is removed from the pull request.

   .. attr:: state

      This is only used for ``pull_request_review`` events.  It
      accepts a list of strings each of which is matched to the review
      state, which can be one of ``approved``, ``comment``, or
      ``request_changes``.

   .. attr:: status

      This is used for ``pull-request`` and ``status`` actions. It
      accepts a list of strings each of which matches the user setting
      the status, the status context, and the status itself in the
      format of ``user:context:status``.  For example,
      ``zuul_github_ci_bot:check_pipeline:success``.

   .. attr: check

      This is only used for ``check_run`` events. It works similar to
      the ``status`` attribute and accepts a list of strings each of
      which matches the app requesting or updating the check run, the
      check run's name and the conclusion in the format of
      ``app:name::conclusion``.
      To make Zuul properly interact with Github's checks API, each
      pipeline that is using the checks API should have at least one
      trigger that matches the pipeline's name regardless of the result,
      e.g. ``zuul:cool-pipeline:.*``. This will enable the cool-pipeline
      to trigger whenever a user requests the ``cool-pipeline`` check
      run as part of the ``zuul`` check suite.
      Additionally, one could use ``.*:success`` to trigger a pipeline
      whenever a successful check run is reported (e.g. useful for
      gating).

   .. attr:: ref

      This is only used for ``push`` events. This field is treated as
      a regular expression and multiple refs may be listed. GitHub
      always sends full ref name, eg. ``refs/tags/bar`` and this
      string is matched against the regular expression.

Reporter Configuration
----------------------
Zuul reports back to GitHub via GitHub API. Available reports include a PR
comment containing the build results, a commit status on start, success and
failure, an issue label addition/removal on the PR, and a merge of the PR
itself. Status name, description, and context is taken from the pipeline.

.. attr:: pipeline.<reporter>.<github source>

   To report to GitHub, the dictionaries passed to any of the pipeline
   :ref:`reporter<reporters>` attributes support the following
   attributes:

   .. attr:: status
      :type: str
      :default: None

      Report status via the Github `status API
      <https://docs.github.com/v3/repos/statuses/>`__.  Set to one of

      * ``pending``
      * ``success``
      * ``failure``

      This is usually mutually exclusive with a value set in
      :attr:`pipeline.<reporter>.<github source>.check`, since this
      reports similar results via a different API.  This API is older
      and results do not show up on the "checks" tab in the Github UI.
      It is recommended to use `check` unless you have a specific
      reason to use the status API.

   .. TODO support role markup in :default: so we can xref
      :attr:`web.status_url` below

   .. attr:: status-url
      :default: link to the build status page
      :type: string

      URL to set in the Github status.

      Defaults to a link to the build status or results page.  This
      should probably be left blank unless there is a specific reason
      to override it.

   .. attr:: check
      :type: string

      Report status via the Github `checks API
      <https://docs.github.com/v3/checks/>`__.  Set to one of

      * ``in_progress``
      * ``success``
      * ``failure``
      *  ``cancelled``

      This is usually mutually exclusive with a value set in
      :attr:`pipeline.<reporter>.<github source>.status`, since this
      reports similar results via a different API.

   .. attr:: comment
      :default: true

      Boolean value that determines if the reporter should add a
      comment to the pipeline status to the github pull request. Only
      used for Pull Request based items.

   .. attr:: review

      One of `approve`, `comment`, or `request-changes` that causes the
      reporter to submit a review with the specified status on Pull Request
      based items. Has no effect on other items.

   .. attr:: review-body

      Text that will be submitted as the body of the review. Required if review
      is set to `comment` or `request-changes`.

   .. attr:: merge
      :default: false

      Boolean value that determines if the reporter should merge the
      pull reqeust. Only used for Pull Request based items.

   .. attr:: label

      List of strings each representing an exact label name which
      should be added to the pull request by reporter. Only used for
      Pull Request based items.

   .. attr:: unlabel

      List of strings each representing an exact label name which
      should be removed from the pull request by reporter. Only used
      for Pull Request based items.

.. _Github App: https://developer.github.com/apps/

Requirements Configuration
--------------------------

As described in :attr:`pipeline.require` and :attr:`pipeline.reject`,
pipelines may specify that items meet certain conditions in order to
be enqueued into the pipeline.  These conditions vary according to the
source of the project in question.  To supply requirements for changes
from a GitHub source named ``my-github``, create a configuration such
as the following::

  pipeline:
    require:
      my-github:
        review:
          - type: approved

This indicates that changes originating from the GitHub connection
named ``my-github`` must have an approved code review in order to be
enqueued into the pipeline.

.. attr:: pipeline.require.<github source>

   The dictionary passed to the GitHub pipeline `require` attribute
   supports the following attributes:

   .. attr:: review

      This requires that a certain kind of code review be present for
      the pull request (it could be added by the event in question).
      It takes several sub-parameters, all of which are optional and
      are combined together so that there must be a code review
      matching all specified requirements.

      .. attr:: username

         If present, a code review from this username is required.  It
         is treated as a regular expression.

      .. attr:: email

         If present, a code review with this email address is
         required.  It is treated as a regular expression.

      .. attr:: older-than

         If present, the code review must be older than this amount of
         time to match.  Provide a time interval as a number with a
         suffix of "w" (weeks), "d" (days), "h" (hours), "m"
         (minutes), "s" (seconds).  Example ``48h`` or ``2d``.

      .. attr:: newer-than

         If present, the code review must be newer than this amount of
         time to match.  Same format as "older-than".

      .. attr:: type

         If present, the code review must match this type (or types).

         .. TODO: what types are valid?

      .. attr:: permission

         If present, the author of the code review must have this
         permission (or permissions).  The available values are
         ``read``, ``write``, and ``admin``.

   .. attr:: open

      A boolean value (``true`` or ``false``) that indicates whether
      the change must be open or closed in order to be enqueued.

   .. attr:: merged

      A boolean value (``true`` or ``false``) that indicates whether
      the change must be merged or not in order to be enqueued.

   .. attr:: current-patchset

      A boolean value (``true`` or ``false``) that indicates whether
      the item must be associated with the latest commit in the pull
      request in order to be enqueued.

      .. TODO: this could probably be expanded upon -- under what
         circumstances might this happen with github

   .. attr:: status

      A string value that corresponds with the status of the pull
      request.  The syntax is ``user:status:value``. This can also
      be a regular expression.

      Zuul does not differentiate between a status reported via
      status API or via checks API (which is also how Github behaves
      in terms of branch protection and `status checks`__).
      Thus, the status could be reported by a
      :attr:`pipeline.<reporter>.<github source>.status` or a
      :attr:`pipeline.<reporter>.<github source>.check`.

      When a status is reported via the status API, Github will add
      a ``[bot]`` to the name of the app that reported the status,
      resulting in something like ``user[bot]:status:value``. For a
      status reported via the checks API, the app's slug will be
      used as is.

   .. __: https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/about-status-checks#types-of-status-checks-on-github

   .. attr:: label

      A string value indicating that the pull request must have the
      indicated label (or labels).

.. attr:: pipeline.reject.<github source>

   The `reject` attribute is the mirror of the `require` attribute.  It
   also accepts a dictionary under the connection name.  This
   dictionary supports the following attributes:

   .. attr:: review

      This takes a list of code reviews.  If a code review matches the
      provided criteria the pull request can not be entered into the
      pipeline.  It follows the same syntax as
      :attr:`pipeline.require.<github source>.review`

Reference pipelines configuration
---------------------------------

Branch protection rules
.......................

The rules prevent Pull requests to be merged on defined branches if they are
not met. For instance a branch might require that specific status are marked
as ``success`` before allowing the merge of the Pull request.

Zuul provides the attribute tenant.untrusted-projects.exclude-unprotected-branches.
This attribute is by default set to ``false`` but we recommend to set it to
``true`` for the whole tenant. By doing so Zuul will benefit from:

 - exluding in-repo development branches used to open Pull requests. This will
   prevent Zuul to fetch and read useless branches data to find Zuul
   configuration files.
 - reading protection rules configuration from the Github API for a given branch
   to define whether a Pull request must enter the gate pipeline. As of now
   Zuul only takes in account "Require status checks to pass before merging" and
   the checked status checkboxes.

With the use of the reference pipelines below, the Zuul project recommends to
set the minimum following settings:

 - attribute tenant.untrusted-projects.exclude-unprotected-branches to ``true``
   in the tenant (main.yaml) configuration file.
 - on each Github repository, activate the branch protections rules and
   configure the name of the protected branches. Furthermore set
   "Require status checks to pass before merging" and check the status labels
   checkboxes (at least ```<tenant>/check```) that must be marked as success in
   order for Zuul to make the Pull request enter the gate pipeline to be merged.


Reference pipelines
...................

Here is an example of standard pipelines you may want to define:

.. literalinclude:: /examples/pipelines/github-reference-pipelines.yaml
   :language: yaml
