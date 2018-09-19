Pylatest
========

Pylatest project consists of set of Docutils_/Sphinx_ extensions which allows
you to:

* Write a description of a test case using `reStructuredText syntax`_.
* Maintain test case descriptions as Sphinx project.
* Include this description into a python source code directly, where it can
  be split into individual sections or actions to be performed, so that the
  description and test automation code are stored next to each other.

The reason behind this is to make synchronization between test case code
and test case description documents simple while keeping the maintenance cost
low in the long term.

Using Pylatest
--------------

The main way to use Pylatest is via Sphinx_ project. See `Pylatest
Documentation`_ for *Quickstart Tutorial* and additional details.

Example
-------

To get better idea what pylatest project looks like, see minimal, but complete,
`Pylatest Demo Project`_. The html builds are available at
https://marbu.gitlab.io/pylatest-demo

Development and testing
-----------------------

For instructions how to install Pylatest from source code or how to run unit
test, see ``HACKING.rst`` file.

Contributions are welcome. See ``CONTRIBUTING.rst`` file for details.

License
-------

Distributed under the terms of the `GNU GPL v3.0`_ license,
pylatest is free and open source software.


.. _`GNU GPL v3.0`: http://www.gnu.org/licenses/gpl-3.0.txt
.. _Docutils: http://docutils.sourceforge.net/
.. _Sphinx: http://www.sphinx-doc.org/en/stable/index.html
.. _`reStructuredText syntax`: http://www.sphinx-doc.org/en/stable/usage/restructuredtext/basics.html
.. _`Pylatest Documentation`: https://pylatest.readthedocs.io/en/stable/
.. _`Pylatest Demo Project`: https://gitlab.com/marbu/pylatest-demo
