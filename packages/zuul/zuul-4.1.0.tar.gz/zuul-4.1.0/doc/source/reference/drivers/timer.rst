:title: Timer Driver

Timer
=====

The timer driver supports triggers only.  It is used for configuring
pipelines so that jobs run at scheduled times.  No connection
configuration is required.

Trigger Configuration
---------------------

Timers don't require a special connection or driver. Instead they can
simply be used by listing ``timer`` as the trigger.

This trigger will run based on a cron-style time specification.  It
will enqueue an event into its pipeline for every project defined in
the configuration.  Any job associated with the pipeline will run in
response to that event.

.. attr:: pipeline.trigger.timer

   The timer trigger supports the following attributes:

   .. attr:: time
      :required:

      The time specification in cron syntax.  Only the 5 part syntax
      is supported, not the symbolic names.  Example: ``0 0 * * *``
      runs at midnight. The first weekday is Monday.
      An optional 6th part specifies seconds.  The optional 7th part
      specifies a jitter in seconds. This advances or delays the
      trigger randomly, limited by the specified value.
      Example ``0 0 * * * * 60`` runs at midnight with a +/- 60
      seconds jitter.
