Test Bar
********

:author: joe.bar@example.com
:caseimportance: high
:comment: This is here just to test metadata processing.

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

.. test_action::
   :step: Do this.
   :result: And this should happen.

Teardown
========

#. Description of the cleanup.

#. There is another one.
