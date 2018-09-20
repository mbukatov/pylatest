.. _pysource:

===============================================
 Extracting Test Cases from Python Source Code
===============================================

.. warning::

   Extraction of test case rst files from python source code via
   ``py2pylatest`` command line tool requires now **deprecated** directives
   :rst:dir:`test_step` and :rst:dir:`test_result`.

   In the future, this will be reimplemented via pytest integration, see:
   https://gitlab.com/mbukatov/pylatest/issues/31

Pylatest also allows you to include test case description into a python source
code directly, where it can be split into individual sections or actions to be
performed, so that the description and test automation code are stored next to
each other.

The reason behind this is to make synchronization between automatic test cases
and test case description documents simple while keeping the maintenance cost
low in the long term.
