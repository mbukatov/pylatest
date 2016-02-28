TODO: name of the testcase
**************************

.. test_metadata:: author ${tc_metadata_author}

Description
===========

TODO: write description of this test case

This file is written in rst file format, if you are not familiar with it,
check:

 * https://en.wikipedia.org/wiki/ReStructuredText
 * http://docutils.sourceforge.net/docs/user/rst/quickref.html
 * http://sphinx-doc.org/rest.html

In addition to that, you can use the following syntax to reference redhat
bugzilla: see :BZ:`439858` (it will create proper link).

Setup
=====

#. TODO: write 1st setup step of this test case

#. TODO: write 2nd setup step of this test case

Test Steps
==========

.. test_step:: 1

    TODO: write 1st test step of this test case, make sure you maintain 4 space
    indentation in the whole text section which describes this step.

    Using code blocks is possible, just maintain indentation properly::

        $$ rpm -q python
        python-2.7.10-8.fc22.x86_64
        $$

.. test_result:: 1

    TODO: write expected result of 1st test step, make sure you maintain 4
    space indentation in the whole text section which describes this result.

Teardown
========

#. TODO: write 1st tear down step of this test case

#. TODO: write 2nd tear down step of this test case
