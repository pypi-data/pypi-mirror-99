============
influxlogger
============

Log PubSubDataMessages (see datastreamcorelib) to InfluxDB, this is a pretty quick and dirty implementation
and definitely not optimal.

For optimal write performance we should add a plugin system that allows
one to convert the payload from the PubSubDataMessages into line-protocol decorated
custom classes https://aioinflux.readthedocs.io/en/stable/usage.html#writing-user-defined-class-objects

The quick-and-dirty optimization is to batch writes into pandas dataframes, which has the not
insignificant drawback of adding pandas/numpy to our requirements.

Docker
------

For more controlled deployments and to get rid of "works on my computer" -syndrome, we always
make sure our software works under docker.

It's also a quick way to get started with a standard development environment.

SSH agent forwarding
^^^^^^^^^^^^^^^^^^^^

We need buildkit_::

    export DOCKER_BUILDKIT=1

.. _buildkit: https://docs.docker.com/develop/develop-images/build_enhancements/

And also the exact way for forwarding agent to running instance is different on OSX::

    export DOCKER_SSHAGENT="-v /run/host-services/ssh-auth.sock:/run/host-services/ssh-auth.sock -e SSH_AUTH_SOCK=/run/host-services/ssh-auth.sock"

and Linux::

    export DOCKER_SSHAGENT="-v $SSH_AUTH_SOCK:$SSH_AUTH_SOCK -e SSH_AUTH_SOCK"

Creating a development container
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Build image, create container and start it (switch the 58770 port to the port from src/influxlogger/defaultconfig.py)::

    docker build --ssh default --target devel_shell -t influxlogger:devel_shell .
    docker create --name influxlogger_devel -p 58770:58770 -v `pwd`":/app" -it -v /tmp:/tmp `echo $DOCKER_SSHAGENT` influxlogger:devel_shell
    docker start -i influxlogger_devel

pre-commit considerations
^^^^^^^^^^^^^^^^^^^^^^^^^

If working in Docker instead of native env you need to run the pre-commit checks in docker too::

    docker exec -i influxlogger_devel /bin/bash -c "pre-commit install"
    docker exec -i influxlogger_devel /bin/bash -c "pre-commit run --all-files"

You need to have the container running, see above. Or alternatively use the docker run syntax but using
the running container is faster::

    docker run -it --rm -v `pwd`":/app" influxlogger:devel_shell -c "pre-commit run --all-files"

Test suite
^^^^^^^^^^

You can use the devel shell to run py.test when doing development, for CI use
the "tox" target in the Dockerfile::

    docker build --ssh default --target tox -t influxlogger:tox .
    docker run -it --rm -v `pwd`":/app" `echo $DOCKER_SSHAGENT` influxlogger:tox

Production docker
^^^^^^^^^^^^^^^^^

There's a "production" target as well for running the application (change "myconfig.toml" for config file)::

    docker build --ssh default --target production -t influxlogger:latest .
    docker run -it --name influxlogger -v myconfig.toml:/app/config.toml -p 58770:58770 -it -v /tmp:/tmp `echo $DOCKER_SSHAGENT` influxlogger:latest


Local Development
-----------------

TLDR:

- Create and activate a Python 3.8 virtualenv (assuming virtualenvwrapper)::

    mkvirtualenv -p `which python3.8` my_virtualenv

- change to a branch::

    git checkout -b my_branch

- install Poetry: https://python-poetry.org/docs/#installation
- Install project deps and pre-commit hooks::

    poetry install
    pre-commit install
    pre-commit run --all-files

- Ready to go, try the following::

    influxlogger --defaultconfig >config.toml
    influxlogger -vv config.toml

Remember to activate your virtualenv whenever working on the repo, this is needed
because pylint and mypy pre-commit hooks use the "system" python for now (because reasons).

Running "pre-commit run --all-files" and "py.test -v" regularly during development and
especially before committing will save you some headache.
