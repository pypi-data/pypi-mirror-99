Prerequisites
-------------

Before you install and configure the python_arista_ccf_neutronclient service,
you must create a database, service credentials, and API endpoints.

#. To create the database, complete these steps:

   * Use the database access client to connect to the database
     server as the ``root`` user:

     .. code-block:: console

        $ mysql -u root -p

   * Create the ``python_arista_ccf_neutronclient`` database:

     .. code-block:: none

        CREATE DATABASE python_arista_ccf_neutronclient;

   * Grant proper access to the ``python_arista_ccf_neutronclient`` database:

     .. code-block:: none

        GRANT ALL PRIVILEGES ON python_arista_ccf_neutronclient.* TO 'python_arista_ccf_neutronclient'@'localhost' \
          IDENTIFIED BY 'PYTHON_ARISTA_CCF_NEUTRONCLIENT_DBPASS';
        GRANT ALL PRIVILEGES ON python_arista_ccf_neutronclient.* TO 'python_arista_ccf_neutronclient'@'%' \
          IDENTIFIED BY 'PYTHON_ARISTA_CCF_NEUTRONCLIENT_DBPASS';

     Replace ``PYTHON_ARISTA_CCF_NEUTRONCLIENT_DBPASS`` with a suitable password.

   * Exit the database access client.

     .. code-block:: none

        exit;

#. Source the ``admin`` credentials to gain access to
   admin-only CLI commands:

   .. code-block:: console

      $ . admin-openrc

#. To create the service credentials, complete these steps:

   * Create the ``python_arista_ccf_neutronclient`` user:

     .. code-block:: console

        $ openstack user create --domain default --password-prompt python_arista_ccf_neutronclient

   * Add the ``admin`` role to the ``python_arista_ccf_neutronclient`` user:

     .. code-block:: console

        $ openstack role add --project service --user python_arista_ccf_neutronclient admin

   * Create the python_arista_ccf_neutronclient service entities:

     .. code-block:: console

        $ openstack service create --name python_arista_ccf_neutronclient --description "python_arista_ccf_neutronclient" python_arista_ccf_neutronclient

#. Create the python_arista_ccf_neutronclient service API endpoints:

   .. code-block:: console

      $ openstack endpoint create --region RegionOne \
        python_arista_ccf_neutronclient public http://controller:XXXX/vY/%\(tenant_id\)s
      $ openstack endpoint create --region RegionOne \
        python_arista_ccf_neutronclient internal http://controller:XXXX/vY/%\(tenant_id\)s
      $ openstack endpoint create --region RegionOne \
        python_arista_ccf_neutronclient admin http://controller:XXXX/vY/%\(tenant_id\)s
