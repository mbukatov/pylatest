.. _quickstart:

===============================
 Getting started with Pylatest
===============================

First of all, Pylatest is a Sphinx_ extension, so check `Sphinx Tutorial`_
first if you are not familiar with Sphinx.


Installation
============

You can install `latest stable Pylatest release from PyPI`_ via pip:

.. code-block:: console

    # pip install pylatest


Installation on Fedora
----------------------

If you use Fedora, you can install rpm packages from `marbu/pylatest copr`_:

.. code-block:: console

    # dnf copr enable marbu/pylatest
    # dnf install python3-pylatest


Installation on RHEL 7
----------------------

If you use RHEL 7 (or other operating system based on RHEL such as CentOS),
install at least ``python-lxml`` package from system repositories,
``python-pip`` from Epel_ and then
install pylatest via pip under normal (non root) user account under which you
are going to use it:

.. code-block:: console

    # yum install python-lxml python-docutils
    # yum --enablerepo=epel install python-pip
    # su - pylatestuser
    $ pip install --user pylatest


Create new Sphinx/Pylatest Project
==================================

First of all you need to create new Sphinx project using ``sphinx-quickstart``
script (see `Sphinx Tutorial`_ for details) and then enable pylatest extension
as shown in the next section.


Adding Pylatest to Existing Sphinx Project
==========================================

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
       :step:
           Run the following commands::

               $ foo --extra sth
               $ bar -vvv

           And wait at least 10 seconds.

       :result:
           Maecenas congue ligula ac quam viverra nec
           consectetur ante hendrerit.

    Teardown
    ========

    #. Description of the cleanup.

    #. There is another one, again.


As you can see from the example above, Pylatest defines custom `docutils
directive`_ named :rst:dir:`test_action` for writing down a test step action (which
includes step itself and expected result). Also note that when the description
of a test step is long and/or complicated, you can use multiple paragraphs to
describe it as shown in the example.

For more details, see description of :ref:`document_type_testcase` structure.


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
.. _`latest stable Pylatest release from PyPI`: https://pypi.org/project/pylatest/
.. _`marbu/pylatest copr`: https://copr.fedorainfracloud.org/coprs/marbu/pylatest/
.. _Epel: https://fedoraproject.org/wiki/EPEL
