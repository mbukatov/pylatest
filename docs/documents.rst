.. _document_types:

=========================
 Pylatest Document Types
=========================

This is an overview of document types supported by Pylatest. For each type,
Pylatest expects particular structure of rst file, list of directives and
roles which could be used and so on.

Test Case
=========

The only document type supported so far. Expected structure in rst file:

* Main heading with *document title*, which is a title of the test case.
* Just after *document title*, there are `docutils field lists`_ with test case
  metadata.
* There are four sections in document: *Description*, *Setup*, *Test Steps*
  and *Teardown* (in this particular order) - of which only *Test Steps* is
  mandatory.
* Section *Test Steps* contains only ``test_action`` directives, which denotes
  test step and expected resutl, and nothing else.


.. _`docutils field lists`: http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html#field-lists
