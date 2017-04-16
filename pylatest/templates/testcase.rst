TODO: name of the testcase
**************************

:author: ${tc_metadata_author}

Description
===========

TODO: write description of this test case

This file is written in rst file format, if you are not familiar with it,
check:

* https://en.wikipedia.org/wiki/ReStructuredText
* http://docutils.sourceforge.net/docs/user/rst/quickref.html
* http://sphinx-doc.org/rest.html

In addition to that, you can use the following syntax to reference redhat
bugzilla: see :RHBZ:`439858` (it will create proper link).

Setup
=====

#. TODO: write 1st setup step of this test case

#. TODO: write 2nd setup step of this test case

Test Steps
==========

.. test_action::
   :step:
       TODO: write 1st test step of this test case, make sure you maintain 4
       space indentation in the whole text section which describes this step.

       Using code blocks is possible, just maintain indentation properly::

           $$ rpm -q python
           python-2.7.10-8.fc22.x86_64
           $$

   :result:
       TODO: write expected result of 1st test step, make sure you maintain 4
       space indentation in the whole text section which describes this result.

.. test_action::
   :step: Use this style when the instructions are short.
   :result: There is no need to use block when it's not needed.

.. test_action::
   :step:
       TODO
   :result:
       TODO

Teardown
========

#. TODO: write 1st tear down step of this test case

#. TODO: write 2nd tear down step of this test case
