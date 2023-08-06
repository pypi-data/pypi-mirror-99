====
GATE
====

Run functions on a remote hub via an http server through a simple API.
This greatly facilitates communication and sharing workloads across nodes in a JSON application.

INSTALLATION
============

.. code-block:: bash

    pip install pop-gate

Get Capabilities
================

Gate extends pop-tree, which can be used to get details of all available resources

.. code-block:: bash

    gate --refs "gate.init.tree"

.. code-block:: bash

    curl http://localhost:5000 -H "Content-Type: application/json" -d '{"ref": "gate.init.tree"}'

USAGE
=====

Run the gate server from the command line and expose specific patterns of hub references.
The '--refs' represent patters on the hub that are allowlisted.
The '--prefix' tells gate to assume that all refs are under a specific dynamic namespace.

In this example we will use a prefix of "gate" and allow all refs under 'hub.gate.init'

.. code-block:: bash

    gate --prefix gate --refs "init.*"

Use curl to run `hub.gate.init.test()` on the remote server like so:

.. code-block:: bash

    curl http://localhost:8080 -H "Content-Type: application/json" -d '{"ref": "init.test"}'

Keyword arguments can be passed by adding extra keys to the call:

.. code-block:: bash

    curl http://localhost:8080 -H "Content-Type: application/json" -d '{"ref": "init.test", "args": ["arg1", "arg2"], "kwargs": {"kwarg1": "value1"}}'

TESTING
=======

Install gate locally with testing libraries:

.. code-block:: bash

    git clone git@gitlab.com:saltstack/pop/gate.git
    pip install -e gate -r requirements-test.txt

Run the tests with pytest

.. code-block:: bash

    pytest gate/tests


INTEGRATION
===========

In order to use gate in your own project add the gate config to your conf.py like so:

my_project/conf.py

.. code-block:: python

    CLI_CONFIG = {
        # Gate options
        "host": {"source": "gate"},
        "port": {"source": "gate"},
        "server": {"source": "gate"},
        "matcher": {"source": "gate"},
        "prefix": {"source": "gate"},
        "refs": {"source": "gate", "default": ["gate.init.test"]},
    }

Add gate startup code to your project's initializer like so:

my_project/my_project/init.py

.. code-block:: python

    def __init__(hub):
        # Horizontally merge the gate dynamic namespace into your project
        hub.pop.sub.add(dyne_name="gate")

    def cli(hub):
        # Load the config from gate onto hub.OPT
        hub.pop.config.load(["my_project", "gate"], cli="my_project")

        # Create the asyncio loop
        hub.pop.loop.create()

        # Get the default gate server, and other options from hub.OPT.gate
        gate_server = hub.OPT.gate.server

        # Create the server coroutine
        coro = hub.gate.init.start(gate_server=gate_server)

        # Start the gate server
        hub.pop.Loop.run_until_complete(coro)
