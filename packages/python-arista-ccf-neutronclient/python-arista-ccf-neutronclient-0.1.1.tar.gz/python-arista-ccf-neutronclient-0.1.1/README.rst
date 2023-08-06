===============================
python-arista-ccf-neutronclient
===============================

Python bindings for Arista Networks Converged Cloud Fabric Neutron API

* Free software: Apache license

Features
--------

- Manually force CCF to sync network configuration

CLI Usage
---------

OpenStack CLI:

- openstack force-ccf-sync
    - Force CCF to sync network configuration
    - No parameter

Neutron CLI (Deprecated):

- neutron force-ccf-sync 1
    - Force CCF to sync network configuration
    - Number 1 is required as parameter