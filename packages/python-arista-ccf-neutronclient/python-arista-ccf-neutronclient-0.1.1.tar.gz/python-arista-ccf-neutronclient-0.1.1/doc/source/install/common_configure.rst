2. Edit the ``/etc/python_arista_ccf_neutronclient/python_arista_ccf_neutronclient.conf`` file and complete the following
   actions:

   * In the ``[database]`` section, configure database access:

     .. code-block:: ini

        [database]
        ...
        connection = mysql+pymysql://python_arista_ccf_neutronclient:PYTHON_ARISTA_CCF_NEUTRONCLIENT_DBPASS@controller/python_arista_ccf_neutronclient
