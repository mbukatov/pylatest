.. _document_types:

=========================
 Pylatest Document Types
=========================

This is an overview of document types supported by Pylatest. For each type,
Pylatest expects particular structure of rst file, list of directives and
roles which could be used and so on. Some rules described there are required
for some pylatest features to work, in other cases it's just matter of
convention.


.. _document_type_testcase:

Test Case
=========

The main Pylatest document type. The rst file of a test case has to follow
structure as described below.

Test Case Title
```````````````

Main heading with *document title* represents a title of a test case, eg.:

.. code-block:: rst

    Test Case Title
    ***************

This title is mandatory.

Test Case Metadata
``````````````````

Just after *document title*, there is a `docutils field list`_ with test
case metadata, eg.:

.. code-block:: rst

    :author: someone@example.com
    :component: foo
    :subcomponent: bar
    :priority: high

Field names of metadata specified here (``author``, ``component``, ...) don't
have to follow any convention, with an exception of requirements.

To **specify requirement covered by a test case**, you need to use either
``requirement`` or ``requirements`` as a field name in this section, eg:

.. code-block:: rst

    :requirement: FOO-123

To specify multiple requirements, you can use a list like this:

.. code-block:: rst

    :requirements:
      - FOO-123
      - FOO-171

It's recommended to reference requirements by url:

.. code-block:: rst

    :requirement: https://example.com/foo-123

Or via :rst:role:`rhbz` role, if there is a bugzilla for it, eg:

.. code-block:: rst

    :requirement: :rhbz:`439858`

Test Case Description
`````````````````````

Description of a test case is represented by dedicated section with title
*Description*, eg.:

.. code-block:: rst

    Description
    ===========

    This is just demonstration of usage of pylatest
    rst directives and expected structure of rst
    document.

Test Case Setup and Teardown
````````````````````````````

There is one section for test setup, and another one for teardown.

In both sections, setup or teardown steps are written down via enumerated list,
eg.:

.. code-block:: rst

    Setup
    =====

    #. This is a first step of the setup.

    #. There is another one.

Test Steps
``````````

Section *Test Steps* contains list of test steps and expected results, written
down using :rst:dir:`test_action` directive.

.. code-block:: rst

    Test Steps
    ==========

    .. test_action::
       :step: List files in the volume: ``ls -a /mnt/helloworld``
       :result: There are no files, output should be empty.

Also note that when the description of a test step is long and/or complicated,
you can use multiple paragraphs to describe it as shown in the example.

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

This section is mandatory.

Full Example
````````````

Here is full example of a test case document based the conventions described
above:

.. code-block:: rst

    Test Case Title
    ***************

    :author: someone@example.com
    :component: foo
    :subcomponent: bar
    :priority: high
    :requirement: https://example.com/foo-123

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


.. _document_type_requirements_overview:

List of requirements
====================

This document provides an overview of all requirements covered by all test
cases in Sphinx/Pylatest project.

The list itself is generated by :rst:dir:`requirementlist` directive.

The expected use case is to generate an overview of requirements for all test
cases like in the following example:

.. code-block:: rst

    Requirements
    ============

    Overview of all requirements covered by test cases.

    .. requirementlist::


.. _`docutils field list`: http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html#field-lists
