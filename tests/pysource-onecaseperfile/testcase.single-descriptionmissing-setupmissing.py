#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""@pylatest
Hello World Test Case
*********************

:author: foo@example.com
:date: 2015-11-06
:comment: This is here just to test metadata processing.

Test Steps
==========

.. test_step:: 1

    List files in the volume: ``ls -a /mnt/helloworld``

.. test_result:: 1

    There are no files, output should be empty.

.. test_step:: 2

    Donec et mollis dolor::

        $ foo --extra sth
        $ bar -vvv

.. test_result:: 2

    Maecenas congue ligula ac quam viverra nec
    consectetur ante hendrerit.

.. test_step:: 3

    This one has no matching test result.

.. test_result:: 4

    And this result has no test step.

Teardown
========

#. Lorem ipsum dolor sit amet: ``rm -rf /mnt/helloworld``.

#. Umount and remove ``lv_helloword`` volume.

#. The end.
"""


import sys


def main():
    print("done")

if __name__ == '__main__':
    sys.exit(main())
