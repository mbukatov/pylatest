=========
 Hacking
=========

This section shows how to run unit tests and how to install latest development
version directly from the source code.


Unit tests
==========

Unit tests are located in ``tests/`` directory and were originally written
using plain unittest_ module from python standard library (without custom
test runners or test suites). Later I decided to switch to pytest_, which can
execute test code written in plain ``unittest`` just fine, but I at least
converted all ``unittest`` asserts calls to ``pytest`` assert statements (this
way, one can use additional ``pytest`` features during debugging of test
failure).

At this point, only small part of unit test code (eg.
``test_xdocutils_nodes.py``) is fully converted to ``pytest``. On the other
hand, any new unit test files should be build using pytest from the start.

To execute all unit tests use predefined tox_ configuration::

    $ tox

The default list of test enviroments executed this way is preconfigured in
``envlist`` option of ``tox.ini`` file.

To use only particular tox test enviroment, for example to
run tests on python3 only, use::

    $ tox -e py35

To use use system installed python packages in tox created virtualenvs, use
sitepackages option (works with both unit tests and flake8 check)::

    $ tox --sitepackages

You can even pass options for pytest from tox as shown in the following
example, where we execute only particular test case in py35 test environment
using system site packages::

    $ tox --sitepackages -e py35 tests/test_xdocutils.py::TestTestActionsTableAutoId::test_teststep_simple

Note that to pass command line options into pytest, one has to use ``--``::

    $ tox -e py35 -- --durations=3 tests/test_rstsource.py::TestFindSections

Very useful is to drop into pdb shell when a test case fails::

    $ tox --sitepackages -e py35 -- --pdb tests/test_rstsource.py


Development Installation
========================

Create new virtualenv environment in root directory of pylatest project (use
path you cloned pylatest git repository into)::

    $ cd ~/projects/pylatest
    $ virtualenv-3.5 --system-site-packages .env

Activate the enviroment::

    $ source .env/bin/activate

And finally, install pylatest in `development mode`_::

    $ pip install -e .

This way, you will have pylatest installed in local virtualenv without messing
with global system or user environment::

    $ cd /tmp
    $ which python
    ~/projects/pylatest/.env/bin/python
    $ which pylatest-rst2html
    ~/projects/pylatest/.env/bin/pylatest-rst2html

Moreover using `development mode`_ allows you to edit files in git repository
and check how it work without reinstallation::

    $ python
    Python 3.5.3 (default, Mar 21 2017, 17:21:33)
    [GCC 6.3.1 20161221 (Red Hat 6.3.1-1)] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import pylatest
    >>> pylatest.__file__
    '/home/martin/projects/pylatest/pylatest/__init__.py'

If you need to test pylatest installed in development mode with Sphinx, you
need to add the following code into ``conf.py`` of sphinx project::

    # If extensions (or modules to document with autodoc) are in another directory,
    # add these directories to sys.path here. If the directory is relative to the
    # documentation root, use os.path.abspath to make it absolute, like shown here.

    import os
    import sys
    sys.path.insert(0, os.path.abspath('/home/martin/projects/pylatest'))

It would work as long as all pylatest dependencies are already installed in
system site packages via distribution packages (rpm, deb ...).


.. _unittest: https://docs.python.org/3.5/library/unittest.html
.. _pytest: http://docs.pytest.org/en/latest/
.. _tox: https://tox.readthedocs.io/en/latest/
.. _`development mode`: https://packaging.python.org/distributing/#working-in-development-mode
