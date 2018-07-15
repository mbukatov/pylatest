.. _restructuredtext:

======================================
 Pylatest reStructuredText Extensions
======================================

This section lists all custom Pylatest extensions of reStructuredText syntax.

Directives
==========

.. rst:directive:: test_action

    Describes test step along with expected result.

    Example:

    .. code-block:: rst

        .. test_action::
           :step: Login as an admin user into Management Console.
           :result: User is authenticated and presented with Admin Dashboard.

    When description of step or result is long and complicated, you can use
    multiple paragraphs to describe it:

    .. code-block:: rst

        .. test_action::
           :step:
               Run the following commands::

                   $ foo --extra sth
                   $ bar -vvv

               And wait at least 10 seconds.

    The directive is used in *Test Steps* section of
    :ref:`document_type_testcase` documents.

.. rst:directive:: .. test_step:: action_id

    Describes just test step part of test action.

    This directive is now **deprecated** and could be removed in next release,
    use :rst:dir:`test_action` directive instead.

.. rst:directive:: .. test_result:: action_id

    Describes just result part of test action.

    This directive is now **deprecated** and could be removed in next release,
    use :rst:dir:`test_action` directive instead.

.. .. rst:directive:: requirement

.. rst:directive:: test_defaults

    This directive, which is usually placed in :ref:`document_type_index`
    document, contains `field list`_ with test case metadata, which are
    enforced for all test cases placed in the same directory tree as the index
    document.

    Example: Let's assume we have subdirectory ``foo`` in Pylatest/Sphinx
    project for test cases of component of the same name. Instead of specifying
    component in each test case file in the directory, we can specify the
    component just once in ``foo/index.rst`` file via this directive:

    .. code-block:: rst

        .. test_defaults::
           :component: foo

    Which will enforce value of component metadata for all test cases in whole
    ``foo`` directory tree, no matter if test cases there contain the metadata
    about component already or not.

.. rst:directive:: requirementlist

    This directive generates list of all requirements which are covered by
    test cases in the Sphinx/Pylatest project, referencing test cases for each
    requirement.

    See :ref:`document_type_testcase` for details how to specify requirements
    in a test case.

Roles
=====

.. rst:role:: rhbz

    A reference to bug from `Red Hat Bugzilla`_. The text "RHBZ number" is
    generated, in the HTML output, this text is a hyperlink to the bug.

    Example:

    .. code-block:: rst

        See :rhbz:`439858` for more details.

.. rst:role:: pylaref

    This role has been removed and is no longer available.

    To create a reference to a test case, use `doc role`_ with absolute
    document name of the test case instead.


.. _`Red Hat Bugzilla`: https://bugzilla.redhat.com/
.. _`field list`: http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html#field-lists
.. _`doc role`: http://www.sphinx-doc.org/en/stable/markup/inline.html#role-doc
