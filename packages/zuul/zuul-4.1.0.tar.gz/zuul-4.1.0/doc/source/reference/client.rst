:title: Zuul Client

Zuul Client
===========

Zuul includes a simple command line client that may be used to affect Zuul's
behavior while running. It must be run on a host that has access to the Gearman
server (e.g., locally on the Zuul host), or on a host with access to Zuul's web
server.

Configuration
-------------

The client uses the same zuul.conf file as the server, and will look
for it in the same locations if not specified on the command line.

If both sections are present, the ``gearman`` section takes precedence over the
``webclient`` section, meaning the client will execute commands using the Gearman
server over the REST API.

It is also possible to run the client without a configuration file, by using the
``--zuul-url`` option to specify the base URL of the Zuul web server.

.. note:: Not all commands are available through the REST API.

Usage
-----
The general options that apply to all subcommands are:

.. program-output:: zuul --help

The following subcommands are supported:

Autohold
^^^^^^^^
.. program-output:: zuul autohold --help

Example::

  zuul autohold --tenant openstack --project example_project --job example_job --reason "reason text" --count 1

Autohold Delete
^^^^^^^^^^^^^^^
.. program-output:: zuul autohold-delete --help

Example::

  zuul autohold-delete --id 0000000123

Autohold Info
^^^^^^^^^^^^^
.. program-output:: zuul autohold-info --help

Example::

  zuul autohold-info --id 0000000123

Autohold List
^^^^^^^^^^^^^
.. program-output:: zuul autohold-list --help

Example::

  zuul autohold-list --tenant openstack

Dequeue
^^^^^^^
.. program-output:: zuul dequeue --help

Examples::

    zuul dequeue --tenant openstack --pipeline check --project example_project --change 5,1
    zuul dequeue --tenant openstack --pipeline periodic --project example_project --ref refs/heads/master

Enqueue
^^^^^^^
.. program-output:: zuul enqueue --help

Example::

  zuul enqueue --tenant openstack --trigger gerrit --pipeline check --project example_project --change 12345,1

Note that the format of change id is <number>,<patchset>.

Enqueue-ref
^^^^^^^^^^^

.. program-output:: zuul enqueue-ref --help

This command is provided to manually simulate a trigger from an
external source.  It can be useful for testing or replaying a trigger
that is difficult or impossible to recreate at the source.  The
arguments to ``enqueue-ref`` will vary depending on the source and
type of trigger.  Some familiarity with the arguments emitted by
``gerrit`` `update hooks
<https://gerrit-review.googlesource.com/admin/projects/plugins/hooks>`__
such as ``patchset-created`` and ``ref-updated`` is recommended.  Some
examples of common operations are provided below.

Manual enqueue examples
***********************

It is common to have a ``release`` pipeline that listens for new tags
coming from ``gerrit`` and performs a range of code packaging jobs.
If there is an unexpected issue in the release jobs, the same tag can
not be recreated in ``gerrit`` and the user must either tag a new
release or request a manual re-triggering of the jobs.  To re-trigger
the jobs, pass the failed tag as the ``ref`` argument and set
``newrev`` to the change associated with the tag in the project
repository (i.e. what you see from ``git show X.Y.Z``)::

  zuul enqueue-ref --tenant openstack --trigger gerrit --pipeline release --project openstack/example_project --ref refs/tags/X.Y.Z --newrev abc123...

The command can also be used asynchronosly trigger a job in a
``periodic`` pipeline that would usually be run at a specific time by
the ``timer`` driver.  For example, the following command would
trigger the ``periodic`` jobs against the current ``master`` branch
top-of-tree for a project::

  zuul enqueue-ref --tenant openstack --trigger timer --pipeline periodic --project openstack/example_project --ref refs/heads/master

Another common pipeline is a ``post`` queue listening for ``gerrit``
merge results.  Triggering here is slightly more complicated as you
wish to recreate the full ``ref-updated`` event from ``gerrit``.  For
a new commit on ``master``, the gerrit ``ref-updated`` trigger
expresses "reset ``refs/heads/master`` for the project from ``oldrev``
to ``newrev``" (``newrev`` being the committed change).  Thus to
replay the event, you could ``git log`` in the project and take the
current ``HEAD`` and the prior change, then enqueue the event::

  NEW_REF=$(git rev-parse HEAD)
  OLD_REF=$(git rev-parse HEAD~1)

  zuul enqueue-ref --tenant openstack --trigger gerrit --pipeline post --project openstack/example_project --ref refs/heads/master --newrev $NEW_REF --oldrev $OLD_REF

Note that zero values for ``oldrev`` and ``newrev`` can indicate
branch creation and deletion; the source code is the best reference
for these more advanced operations.


Promote
^^^^^^^

.. program-output:: zuul promote --help

Example::

  zuul promote --tenant openstack --pipeline gate --changes 12345,1 13336,3

Note that the format of changes id is <number>,<patchset>.

The promote action is used to reorder the change queue in a pipeline, by putting
the provided changes at the top of the queue; therefore this action makes the
most sense when performed against a dependent pipeline.

The most common use case for the promote action is the need to merge an urgent
fix when the gate pipeline has already several patches queued ahead. This is
especially needed if there is concern that one or more changes ahead in the queue
may fail, thus increasing the time to land for the fix; or concern that the fix
may not pass validation if applied on top of the current patch queue in the gate.

If the queue of a dependent pipeline is targeted by the promote, all the ongoing
jobs in that queue will be canceled and restarted on top of the promoted changes.

Show
^^^^

.. note:: This command is only available through a Gearman connection.

.. program-output:: zuul show --help

Example::

  zuul show running-jobs

tenant-conf-check
^^^^^^^^^^^^^^^^^

.. note:: This command is only available through a Gearman connection.

.. program-output:: zuul tenant-conf-check --help

Example::

  zuul tenant-conf-check

This command validates the tenant configuration schema. It exits '-1' in
case of errors detected.

create-auth-token
^^^^^^^^^^^^^^^^^

.. note:: This command is only available if an authenticator is configured in
          ``zuul.conf``. Furthermore the authenticator's configuration must
          include a signing secret.

.. program-output:: zuul create-auth-token --help

Example::

    zuul create-auth-token --auth-config zuul-operator --user alice --tenant tenantA --expires-in 1800

The return value is the value of the ``Authorization`` header the user must set
when querying a protected endpoint on Zuul's REST API.

Example::

    bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwOi8vbWFuYWdlc2Yuc2ZyZG90ZXN0aW5zdGFuY2Uub3JnIiwienV1bC50ZW5hbnRzIjp7ImxvY2FsIjoiKiJ9LCJleHAiOjE1Mzc0MTcxOTguMzc3NTQ0fQ.DLbKx1J84wV4Vm7sv3zw9Bw9-WuIka7WkPQxGDAHz7s
