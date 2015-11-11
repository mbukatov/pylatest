This section shows how to install latest development version directly from
source code.

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
