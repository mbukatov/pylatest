.. _cli:

=============================
 Pylatest Command Line Tools
=============================

Pylatest command line tools can be classified into several groups.


Docutils Front End Tools
========================

Tools with name matching ``pylatest-rst2*`` are simple wrappers of `docutils
front-end tools`_ with Pylatest extensions enabled (they behave in the same
way, accept the same command line options):

* ``pylatest-rst2html`` produces html output for human consumption
* ``pylatest-rst2htmlplain`` produces scripting friendly html output
* ``pylatest-rst2pseudoxml`` produces pseudoxml version of parsing friendly
  plain output

Note that they are expected to be used mainly for debugging/testing and some
features may be missing compated to Sphinx module described above, which is the
primary way to use Pylatest. Moreover neither html nor html plain output fully
mach the output produced by Sphinx even when missing features are not used.


Preview
=======

Tool ``pylatest-preview`` produces a man page representation of given
pylatest rst file and shows it using ``/usr/bin/man``. This is useful for
quick checking of rst file from command line. It's basically equivalent to
``pylatest-rst2man testcase.rst | man -l -`` and for this reason the same
limitations as for other pylatest wrappers of docutils front-end tools apply.


Python Extractor
================

Python source code extractor ``py2pylatest`` can generate rst file
from python source code with pylatest string literals.


Others
======

Various other helpers, such as (currently incomplete) ``pylatest-template``.


.. _`docutils front-end tools`: http://docutils.sourceforge.net/docs/user/tools.html
