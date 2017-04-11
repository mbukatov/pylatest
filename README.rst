Pylatest
========

Pylatest project consists of set of Docutils_/Sphinx_ extensions and related
tools which allows you to:

* Write a description of a test case using `reStructuredText syntax`_.
* Maintain test case description as Sphinx project.
* Include this description into a python source code directly, where it can
  be split into individual sections or actions to be performed, so that the
  description and test automation code are stored next to each other.

The reason behind this is to make synchronization between automatic test cases
and test case description documents simple while keeping the maintenance cost
low in the long term.

Using Pylatest
--------------

The main way to use Pylatest is via Sphinx_ project.

You can start a new Sphinx/Pylatest project using the quickstart script::

    $ pylatest-quickstart

This very simple wrapper of ``sphinx-quickstart`` will generate initial Sphinx
project with pylatest extension enabled and few configuration values predefined
(eg. ``Makefile`` will be always generated) having Pylatest use case in mind.

To use Pylatest with your existing sphinx project, add ``pylatest``
module into list of extensions in ``conf.py`` of the project::

    extensions = [
        'pylatest',
        ]

Pylatest Command Line Tools
---------------------------

Pylatest command line tools can be classified into several groups:

* Already mentioned ``pylatest-quickstart`` is a simple wrapper of
  ``sphinx-quickstart`` tool for starting new Sphinx/Pylatest project.
* Docutils wrappers ``pylatest-rst*`` (eg. ``pylatest-rst2html`` or
  ``pylatest-rst2pseudoxml``). These are simple wrappers of `docutils front-end
  tools`_ with Pylatest extensions enabled. Note that they are expected
  to be used mainly for debugging/testing and some features may be missing
  compated to Sphinx module described above, which is the primary way to use
  Pylatest.
* Tool ``pylatest-preview`` produces a man page representation of given
  pylatest rst file and shows it using ``/usr/bin/man``. This is useful for
  quick checking of rst file from command line. It's basically equivalent to
  ``pylatest-rst2man testcase.rst | man -l -`` and for this reason the same
  limitations as for other pylatest wrappers of docutils front-end tools apply.
* Python source code extractor ``py2pylatest`` which can generate rst file
  from python source code with pylatest string literals.
* Various helpers (eg. ``pylatest-template``).

Development and testing
-----------------------

For instructions how to install pylatest from source code or how to run unit
test, see ``HACKING.rst``.

License
-------

Distributed under the terms of the `GNU GPL v3.0`_ license,
pylatest is free and open source software.


.. _`GNU GPL v3.0`: http://www.gnu.org/licenses/gpl-3.0.txt
.. _Docutils: http://docutils.sourceforge.net/
.. _Sphinx: http://www.sphinx-doc.org/en/stable/index.html
.. _`reStructuredText syntax`: http://www.sphinx-doc.org/en/stable/rest.html
.. _`docutils front-end tools`: http://docutils.sourceforge.net/docs/user/tools.html
