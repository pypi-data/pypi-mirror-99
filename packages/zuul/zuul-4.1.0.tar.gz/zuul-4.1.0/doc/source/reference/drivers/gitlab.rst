:title: GitLab Driver

.. _gitlab_driver:

GitLab
======

The GitLab driver supports sources, triggers, and reporters. It can
interact with the public GitLab.com service as well as site-local
installations of GitLab.

Configure GitLab
----------------

Zuul needs to interact with projects by:

- receiving events via web-hooks
- performing actions via the API

The Zuul user's API token configured in zuul.conf must have the
following ACL rights: "api". The API token must be created in user Settings,
Access tokens.

Each project to be integrated with Zuul needs in "Settings/Webhooks":

- "URL" set to
  ``http://<zuul-web>/zuul/api/connection/<conn-name>/payload``
- "Merge request events" set to "on"
- "Push events" set to "on"
- "Tag push events" set to "on"
- "Comments" set to "on"
- Define a "Secret Token"

Connection Configuration
------------------------

The supported options in ``zuul.conf`` connections are:

.. attr:: <gitlab connection>

   .. attr:: driver
      :required:

      .. value:: gitlab

         The connection must set ``driver=gitlab`` for GitLab connections.

   .. attr:: api_token

      The user's API token.

   .. attr:: webhook_token

      The project's webhook secret token.

   .. attr:: server
      :default: gitlab.com

      Hostname of the GitLab server.

   .. attr:: canonical_hostname

      The canonical hostname associated with the git repos on the
      GitLab server.  Defaults to the value of :attr:`<gitlab
      connection>.server`.  This is used to identify projects from
      this connection by name and in preparing repos on the filesystem
      for use by jobs.  Note that Zuul will still only communicate
      with the GitLab server identified by **server**; this option is
      useful if users customarily use a different hostname to clone or
      pull git repos so that when Zuul places them in the job's
      working directory, they appear under this directory name.

   .. attr:: baseurl
      :default: https://{server}

      Path to the GitLab web and API interface.

   .. attr:: cloneurl
      :default: {baseurl}

      Path to the GitLab Git repositories. Used to clone.


Trigger Configuration
---------------------

GitLab webhook events can be configured as triggers.

A connection name with the GitLab driver can take multiple events with
the following options.

.. attr:: pipeline.trigger.<gitlab source>

   The dictionary passed to the GitLab pipeline ``trigger`` attribute
   supports the following attributes:

   .. attr:: event
      :required:

      The event from GitLab. Supported events are:

      .. value:: gl_merge_request

      .. value:: gl_push

   .. attr:: action

      A :value:`pipeline.trigger.<gitlab source>.event.gl_merge_request`
      event will have associated action(s) to trigger from. The
      supported actions are:

      .. value:: opened

         Merge request opened.

      .. value:: changed

         Merge request synchronized.

      .. value:: merged

         Merge request merged.

      .. value:: comment

         Comment added to merge request.

      .. value:: approved

         Merge request approved.

      .. value:: unapproved

         Merge request unapproved.

      .. value:: labeled

         Merge request labeled.

   .. attr:: comment

      This is only used for ``gl_merge_request`` and ``comment`` actions.  It
      accepts a list of regexes that are searched for in the comment
      string. If any of these regexes matches a portion of the comment
      string the trigger is matched.  ``comment: retrigger`` will
      match when comments containing 'retrigger' somewhere in the
      comment text are added to a merge request.

   .. attr:: labels

      This is only used for ``gl_merge_request`` and ``labeled`` actions.  It
      accepts a string or a list of strings that are searched into the list
      of labels set to the merge request.

   .. attr:: ref

      This is only used for ``gl_push`` events. This field is treated as
      a regular expression and multiple refs may be listed. GitLab
      always sends full ref name, eg. ``refs/heads/bar`` and this
      string is matched against the regular expression.


Reporter Configuration
----------------------
Zuul reports back to GitLab via the API. Available reports include a Merge Request
comment containing the build results. Status name, description, and context
is taken from the pipeline.

.. attr:: pipeline.<reporter>.<gitlab source>

   To report to GitLab, the dictionaries passed to any of the pipeline
   :ref:`reporter<reporters>` attributes support the following
   attributes:

   .. attr:: comment
      :default: true

      Boolean value that determines if the reporter should add a
      comment to the pipeline status to the GitLab Merge Request.

   .. attr:: approval

      Bolean value that determines whether to report *approve* or *unapprove*
      into the merge request approval system. To set an approval the Zuul user
      must be a *Developer* or *Maintainer* project's member. If not set approval
      won't be reported.

   .. attr:: merge
      :default: false

      Boolean value that determines if the reporter should merge the
      Merge Request. To merge a Merge Request the Zuul user must be a *Developer* or
      *Maintainer* project's member. In case of *developer*, the *Allowed to merge*
      setting in *protected branches* must be set to *Developers + Maintainers*.


Requirements Configuration
--------------------------

As described in :attr:`pipeline.require` pipelines may specify that items meet
certain conditions in order to be enqueued into the pipeline.  These conditions
vary according to the source of the project in question.

.. code-block:: yaml

   pipeline:
     require:
       gitlab:
         open: true

This indicates that changes originating from the GitLab connection must be
in the *opened* state (not merged yet).

.. attr:: pipeline.require.<gitlab source>

   The dictionary passed to the GitLab pipeline `require` attribute
   supports the following attributes:

   .. attr:: open

      A boolean value (``true`` or ``false``) that indicates whether
      the Merge Request must be open in order to be enqueued.

   .. attr:: merged

      A boolean value (``true`` or ``false``) that indicates whether
      the Merge Request must be merged or not in order to be enqueued.

   .. attr:: approved

      A boolean value (``true`` or ``false``) that indicates whether
      the Merge Request must be approved or not in order to be enqueued.

   .. attr:: labels

      if present, the list of labels a Merge Request must have.


Reference pipelines configuration
---------------------------------

Here is an example of standard pipelines you may want to define:

.. literalinclude:: /examples/pipelines/gitlab-reference-pipelines.yaml
   :language: yaml
