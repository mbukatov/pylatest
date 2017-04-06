Pylatest
========

Pylatest project provides a set of tools which allows you to:

* Write a description of a test case using reStructuredText syntax.
* Include this description into a python source code directly, where it can
  be split into individual sections or actions to be performed, so that the
  description and test automation code are stored next to each other.

The reason behind this is to make synchronization between automatic test cases
and test case description documents simple while keeping the maintenance cost
low in the long term.

Pylatest Tools
--------------

Pylatest command line tools can be classified into several groups:

* ``pylatest2html`` and ``pylatest2htmlplain``: custom docutils clients
  which uses several docutils extensions (custom pylatest directives,
  roles, transformations ...)
* ``py2pylatest`` python source code extractor which can generate rst file
  from python source code with pylatest string literals
* various helpers (eg. ``pylatest-template``)

Development and testing
-----------------------

For instructions how to install pylatest from source code or how to run unit
test, see ``HACKING.rst``.

License
-------

Distributed under the terms of the `GNU GPL v3.0`_ license,
pylatest is free and open source software.


.. _`GNU GPL v3.0`: http://www.gnu.org/licenses/gpl-3.0.txt
