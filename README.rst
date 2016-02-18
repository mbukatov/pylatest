Pylatest
========

Pylatest project provides a set of tools which allows you to:

* Write a description of a test case using reStructuredText syntax.
* Include this description into a python source code directly, split into
  individual sections or actions to be performed, so that the description and
  test automation code are stored next to each other.

The reason behind this is to make synchronization between automatic test cases
and test case description simple and to keep it's maintenance cost low in a
long term.

Pylatest tools can be classified into several groups:

* ``pylatest2html`` and ``pylatest2htmlplain``: custom docutils clients
  which uses several docutils extensions (custom pylatest directives,
  roles, transformations ...)
* ``py2pylatest`` python source code extractor which can generate rst file
  from python source code with pylatest string literals
* various helpers (eg. ``pylatest-template``)

Sphinx
------

To use pylatest directives in a sphinx project, you need to register them into
docutils rst parser in a similar way as it's done in ``pylatest2html``
command line client. Assuming you have pylatest installed properly (so that
you can import pylatest module without any problems), add following lines
into ``conf.py`` of your sphinx project::

    import pylatest.client

    pylatest.client.register_table()

Development and testing
-----------------------

For instructions how to install pylatest from source code, see ``HACKING.rst``.
