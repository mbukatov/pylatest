Test Bar
********

:author: joe.bar@example.com
:requirement: :rhbz:`439858`

Test Steps
==========

.. test_action::
   :step: List files in the volume: ``ls -a /mnt/helloworld``
   :result: There are no files, output should be empty.
