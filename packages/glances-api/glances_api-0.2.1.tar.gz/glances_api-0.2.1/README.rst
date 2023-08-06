python-glances-api
==================

A Python client for interacting with `Glances <https://nicolargo.github.io/glances/>`_.

This module is not official, developed, supported or endorsed by Glances.

Installation
------------

The module is available from the `Python Package Index <https://pypi.python.org/pypi>`_.

.. code:: bash

    $ pip3 install glances_api

Or on a Fedora-based system or on a CentOS/RHEL machine with has EPEL enabled.

.. code:: bash

    $ sudo dnf -y install python3-glances-api

Usage
-----

The file ``example.py`` contains an example about how to use this module.

Development
-----------

For development is recommended to use a ``venv``.

.. code:: bash

    $ python3 -m venv .
    $ source bin/activate
    $ python3 setup.py develop

License
-------

``python-glances-api`` is licensed under MIT, for more details check LICENSE.
