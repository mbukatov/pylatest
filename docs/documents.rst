.. _document_types:

=========================
 Pylatest Document Types
=========================

This is an overview of document types supported by Pylatest. For each type,
Pylatest expects particular structure of rst file, list of directives and
roles which could be used and so on. Following descriptions there is required
for some features to work, sometimes it's just matther of convention.

.. _document_type_testcase:

Test Case
=========

The main Pylatest document type. Expected structure of test case rst
file:

* Main heading with *document title*, which is a title of the test case.
* Just after *document title*, there are `docutils field lists`_ with test case
  metadata.
* There are four sections in document: *Description*, *Setup*, *Test Steps*
  and *Teardown* (in this particular order) - of which only *Test Steps* is
  mandatory.
* Section *Test Steps* contains only :rst:dir:`test_action` directives and
  nothing else.

.. _document_type_index:

Index
=====

Index file (usually named ``index.rst``) represents all test cases placed in
the same directory as the index file.

Subdirectories with index file could be used to group test cases together and
enforce particular metadata on the whole group via :rst:dir:`test_defaults`
directive.

Usual use case is to create subdirectory with ``index.rst`` file for particular
component like this:

.. code-block:: rst

    Foo Component
    =============

    .. test_defaults::
       :component: foo

    .. toctree::
       :caption: Test Cases
       :maxdepth: 1
       :glob:

       test_*

So that html build of index file will contain list of all test cases there
and enforce particular value of ``:component:`` metadata on all test cases
at the same time.


.. _`docutils field lists`: http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html#field-lists
