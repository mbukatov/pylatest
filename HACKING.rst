This section shows how to install latest development version directly from
the source code.

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

Installation into virtualenv
============================

Create new virtualenv environment in root directory of pylatest project (use
path you cloned pylatest git repository into)::

    cd ~/projects/pylatest
    virtualenv .env

Activate the enviroment::

    source .env/bin/activate

And finally, install pylatest::

    python setup.py install

This way, you will have pylatest installed in local virtualenv without messing
with global system or user environment::

    $ cd /tmp
    $ which python
    ~/projects/pylatest/.env/bin/python
    $ which pylatest2html 
    ~/projects/pylatest/.env/bin/pylatest2htm
    $ python
    Python 2.7.10 (default, Sep 24 2015, 17:49:29) 
    [GCC 5.1.1 20150618 (Red Hat 5.1.1-4)] on linux2
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import pylatest
    >>> pylatest.__file__
    '/home/martin/projects/pylatest/.env/lib/python2.7/site-packages/pylatest-0.1-py2.7.egg/pylatest/__init__.pyc'


.. _unittest: https://docs.python.org/3.5/library/unittest.html
.. _pytest: http://docs.pytest.org/en/latest/
.. _tox: https://tox.readthedocs.io/en/latest/
