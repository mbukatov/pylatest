Test Baz
********

:author: joe.doe@example.com
:casesubcomponent: baz
:caseimportance: low

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
   :step: Do this.
   :result: And this should happen.

.. test_action::
   :step: And this.
   :result: Nothing happens at this point.

Teardown
========

#. Description of the cleanup.

#. There is another one.
