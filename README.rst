Pylatest
========

Set of tools (docutils wrappers, custom rst directives) generating testcase
descriptions from source files written in reStructuredText.

This project is in early stage of development.
There is not much to be seen so far ...

Sphinx
------

To use pylatest directives in sphinx project, you need to register them into
docutils rst parser in a similar way as it's done in ``pylatest2html``
command line client. Assuming you have pylatest installed properly (so that
you can import pylatest module without any problems), add following lines
into ``conf.py`` of your sphinx project::

    import pylatest.client

    pylatest.client.register_directives()

Development and testing
-----------------------

This section shows how to install latest development version directly from
source code.

First of all, clone git repository::

    git clone https://github.com/marbu/pylatest.git
    cd pylatest

Create new virtualenv environment and activate it::

    virtualenv .env
    source .env/bin/activate

And finally, install pylatest::

    python setup.py install

This way, you will have pylatest installed in local virtualenv without messing
with global system or user environment::

    $ cd /tmp
    $ which python
    ~/tvorba/pylatest/.env/bin/python
    $ which pylahello.py 
    ~/tvorba/pylatest/.env/bin/pylahello.py
    $ python
    Python 2.7.10 (default, Sep 24 2015, 17:49:29) 
    [GCC 5.1.1 20150618 (Red Hat 5.1.1-4)] on linux2
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import pylatest
    >>> pylatest.__file__
    '/home/martin/tvorba/pylatest/.env/lib/python2.7/site-packages/pylatest-0.1-py2.7.egg/pylatest/__init__.pyc'
