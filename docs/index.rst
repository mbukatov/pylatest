.. Pylatest documentation master file, created by
   sphinx-quickstart on Thu Apr 27 17:58:47 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

==========
 Pylatest
==========

Pylatest project consists of set of Docutils_/Sphinx_ extensions and related
command line tools which allows you to:

* Write a description of a test case using `reStructuredText syntax`_.
* Maintain test case descriptions as Sphinx project.
* Include this description into a python source code directly, where it can
  be split into individual sections or actions to be performed, so that the
  description and test automation code are stored next to each other.

The reason behind this is to make synchronization between test case code
and test case description documents simple while keeping the maintenance cost
low in the long term.


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   quickstart.rst
   documents.rst
   restructuredtext.rst
   cli.rst
   xmlexport.rst
   pysource.rst


License
=======

Distributed under the terms of the `GNU GPL v3.0`_ license,
Pylatest is free and open source software.


Related Projects
================

* Docutils_
* Sphinx_
* Betelgeuse_
* Testimony_
* Polarize_
* Pong_
* `Pytest Polarion`_
* `Pytest Polarion CFME`_


.. _`reStructuredText syntax`: http://www.sphinx-doc.org/en/stable/rest.html
.. _`GNU GPL v3.0`: http://www.gnu.org/licenses/gpl-3.0.txt
.. _Docutils: http://docutils.sourceforge.net/
.. _Sphinx: http://www.sphinx-doc.org/en/stable/index.html
.. _Betelgeuse: https://betelgeuse.readthedocs.io/en/latest/
.. _Testimony: https://testimony-qe.readthedocs.io/en/stable/
.. _Polarize: https://github.com/RedHatQE/polarize
.. _Pong: https://github.com/RedHatQE/pong
.. _`Pytest Polarion`: https://github.com/avi3tal/pytest-polarion
.. _`Pytest Polarion CFME`: https://github.com/mkoura/pytest-polarion-cfme
