drops
=====

Distributed execution system

Getting Started
===============

*NOTE:* This instructions assume you have redis-server running on localhost:6379


Create a virtual environment first, then:

  python setup.py develop


Start a few workers:

   $ drops-server --listen 'tcp://127.0.0.1:5556' --workers drops.worker.console

   $ drops-server --listen 'tcp://127.0.0.1:5557' --workers drops.worker.console

Start main scheduler:

   $ drops-server # Will listen on 5555


Now, spawn some commands:

    >>> from smartrpyc import Client
    >>> c = Client("tcp://127.0.0.1:5555")
    >>> c.log("test")

Details
=======

`c.log` executes an `rpc` call to the master scheduler - on port 5555 - which looks for a valid worker to consume that command. Workers register themselves into Redis (this is the default back-end, although, other back-ends can be used implemented)


Client -> Scheduler -> Redis -> Scheduler -> Worker -> Scheduler -> Client
