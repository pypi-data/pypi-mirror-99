.. _install-rdo:

Install and configure for Red Hat Enterprise Linux and CentOS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


This section describes how to install and configure the python_arista_ccf_neutronclient service
for Red Hat Enterprise Linux 7 and CentOS 7.

.. include:: common_prerequisites.rst

Install and configure components
--------------------------------

#. Install the packages:

   .. code-block:: console

      # yum install

.. include:: common_configure.rst

Finalize installation
---------------------

Start the python_arista_ccf_neutronclient services and configure them to start when
the system boots:

.. code-block:: console

   # systemctl enable openstack-python_arista_ccf_neutronclient-api.service

   # systemctl start openstack-python_arista_ccf_neutronclient-api.service
