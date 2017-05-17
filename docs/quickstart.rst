.. _quickstart:

===============================
 Getting started with Pylatest
===============================

First of all, Pylatest is a Sphinx_ extension, so check `Sphinx Tutorial`_
first if you are not familiar with Sphinx.


Installation
============

You can install latest stable Pylatest release from PyPI via pip:

.. code-block:: sh

    $ pip install pylatest

.. note::

    This doesn't work right now because no stable release has been published
    on PyPI yet, see HACKING.rst file for instructions how to install from
    source code in the mean time.

.. note:: TODO

    Link to rpm copr builds for Fedora and RHEL when available.


Create new Sphinx/Pylatest Project
==================================

You can start a new Sphinx/Pylatest project using the quickstart script:

.. code-block:: sh

    $ pylatest-quickstart

This very simple wrapper of ``sphinx-quickstart`` will generate initial Sphinx
project with pylatest extension enabled and few configuration values predefined
(eg. ``Makefile`` will be always generated) having Pylatest use case in mind.


Adding Pylatest to Existing Project
===================================

To use Pylatest with your existing Sphinx project, add ``pylatest``
module into list of extensions in ``conf.py`` of the project:

.. code-block:: python

    extensions = [
        'pylatest',
        ]


Writing Test Cases
==================

When you have Sphinx project with Pylatest extension enabled, you can start
writing test cases. Pylatest expects that a test case is located in dedicated
rst file, you should not describe multiple test cases in single file. Other
aspects of structure of pylatest/sphinx project is completelly up to you
though.

Pylatest test case document should follow this structure:

* Document tile is a title of the test case.
* Just after document title, there are `docutils field lists`_ with test case
  metadata.
* There are four sections in document: *Description*, *Setup*, *Test Steps*
  and *Teardown* - of which only *Test Steps* is mandatory.
* Section *Test Steps* contains custom pylatest syntax for test steps, we
  will discuss this in more detail shortly.

Here is an example of a test case document following expected structure:

.. code-block:: rst

    Test Case Title
    ***************

    :author: someone@example.com
    :component: foo
    :subcomponent: bar
    :priority: high

    Description
    ===========

    This is just demonstration of usage of pylatest
    rst directives and expected structure of rst
    document.

    Setup
    =====

    #. This is a first step of the setup.

    #. There is another one.

    Test Steps
    ==========

    .. test_action::
       :step: List files in the volume: ``ls -a /mnt/helloworld``
       :result: There are no files, output should be empty.

    .. test_action::
       :step: Another test step.
       :result: Yet another expected result.

    Teardown
    ========

    #. Description of the cleanup.

    #. There is another one, again.


As you can see from the example above, Pylatest defines custom `docutils
directive`_ named ``test_action`` for writing down a test step action (which
includes step itself and expected result):

.. code-block:: rst

    .. test_action::
       :step: Here goes what should be done.
       :result: Here is the expected result of previous action.

Note that when the description of a test step is long and/or complicated, you
can use multiple paragraphs to describe it:

.. code-block:: rst

    .. test_action::
       :step:
           Run the following commands::

               $ foo --extra sth
               $ bar -vvv

           And wait at least 10 seconds.

       :result:
           Maecenas congue ligula ac quam viverra nec
           consectetur ante hendrerit.


HTML output
===========

To generate html output, run ``make html`` in the root directory of
sphinx/pylatest project as one would do with any other sphinx project.

Note that default pylatest html builder produces human readable representation
of a test case, which generates table from all ``test_action`` directives from
*Test Steps* section.

For example, following rst source:

.. code-block:: rst

    .. test_action::
       :step: Foo Step.
       :result: Foo Result.

    .. test_action::
       :step: Bar Step.
       :result: Bar Result.

Would be represented in the following way in html output:

+---+------------+-----------------+
|   | Step       | Expected Result |
+===+============+=================+
| 1 | Foo Step.  | Foo Result.     |
+---+------------+-----------------+
| 2 | Bar Step.  | Bar Result.     |
+---+------------+-----------------+


.. _Sphinx: http://www.sphinx-doc.org/en/stable/index.html
.. _`Sphinx Tutorial`: http://www.sphinx-doc.org/en/stable/tutorial.html
.. _`docutils field lists`: http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html#field-lists
.. _`docutils directive`: http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html#directives
