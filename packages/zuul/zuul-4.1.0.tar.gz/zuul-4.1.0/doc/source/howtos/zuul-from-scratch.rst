Zuul From Scratch
=================

This document details a fully manual installation of Zuul on a
all-in-one server.  If you want to learn all the details about how to
install Zuul without the aid of any existing installation tools, you
may find this a useful reference.

If, instead, you want to get Zuul running quickly, see the
:ref:`quick_start` which runs all of the Zuul services in containers
with a single command.

Environment Setup
-----------------

Follow the instructions below, depending on your server type.

  * :doc:`fedora27_setup`
  * :doc:`centos7_setup`
  * :doc:`opensuse_leap15_setup`
  * :doc:`ubuntu_setup`

Installation
------------

  * :doc:`nodepool_install`
  * :doc:`zuul_install`

Configuration
-------------

Nodepool
~~~~~~~~

Nodepool can support different backends. Select the configuration for
your installation.

  * :doc:`nodepool_openstack`
  * :doc:`nodepool_static`

Zuul
~~~~

Write the Zuul config file.  Note that this configures Zuul's web
server to listen on all public addresses.  This is so that Zuul may
receive webhook events from GitHub.  You may wish to proxy this or
further restrict public access.  You should set the GIT_USER variables
to appropriate values for your setup.

.. code-block:: shell

   export GIT_USER_NAME=CHANGE ME
   export GIT_USER_EMAIL=change@me.com
   sudo --preserve-env=GIT_USER_NAME,GIT_USER_EMAIL bash -c \
   "cat > /etc/zuul/zuul.conf <<EOF
   [gearman]
   server=127.0.0.1

   [gearman_server]
   start=true

   [zookeeper]
   hosts=localhost

   [executor]
   private_key_file=/var/lib/zuul/.ssh/nodepool_rsa

   [merger]
   git_user_name=$GIT_USER_NAME
   git_user_email=$GIT_USER_EMAIL

   [web]
   listen_address=0.0.0.0

   [scheduler]
   tenant_config=/etc/zuul/main.yaml
   EOF"

   sudo bash -c "cat > /etc/zuul/main.yaml <<EOF
   - tenant:
       name: quickstart
   EOF"

Starting Services
-----------------

After you have Zookeeper, Nodepool, and Zuul installed and configured, you can
start Nodepool and Zuul services with::

   sudo systemctl daemon-reload

   sudo systemctl start nodepool-launcher.service
   sudo systemctl status nodepool-launcher.service
   sudo systemctl enable nodepool-launcher.service

   sudo systemctl start zuul-scheduler.service
   sudo systemctl status zuul-scheduler.service
   sudo systemctl enable zuul-scheduler.service
   sudo systemctl start zuul-executor.service
   sudo systemctl status zuul-executor.service
   sudo systemctl enable zuul-executor.service
   sudo systemctl start zuul-web.service
   sudo systemctl status zuul-web.service
   sudo systemctl enable zuul-web.service

Use Zuul Jobs
-------------

Zuul provides a `standard library`_ of jobs and roles.  To take advantage
of these jobs, add the ``zuul-jobs`` repo, which is hosted by the Zuul
project, to your system.

Add to ``/etc/zuul/zuul.conf``:

.. code-block:: shell

   sudo bash -c "cat >> /etc/zuul/zuul.conf <<EOF

   [connection zuul-git]
   driver=git
   baseurl=https://opendev.org/
   EOF"

Restart executor and scheduler:

.. code-block:: shell

   sudo systemctl restart zuul-executor.service
   sudo systemctl restart zuul-scheduler.service

.. _standard library: https://zuul-ci.org/docs/zuul-jobs/

Setup Your Repo
---------------

Select your code repository to setup.

  * :doc:`gerrit_setup`
  * :doc:`github_setup`
