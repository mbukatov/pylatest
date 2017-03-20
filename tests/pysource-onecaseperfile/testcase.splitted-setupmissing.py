#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""@pylatest
Hello World Test Case
*********************

:author: foo@example.com
:date: 2015-11-06
:comment: This is here just to test metadata processing.
"""

"""@pylatest
Description
===========

This is just demonstration of usage of pylatest rst directives and expected
structure of rst document.

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec a diam lectus.
Sed sit amet ipsum mauris. Maecenas congue ligula ac quam viverra nec
consectetur ante hendrerit. Donec et mollis dolor. Praesent et diam eget libero
egestas mattis sit amet vitae augue.

See :RHBZ:`439858` for more details.
"""

"""@pylatest
.. test_step:: 1

    List files in the volume: ``ls -a /mnt/helloworld``
"""

"""@pylatest
.. test_result:: 1

    There are no files, output should be empty.
"""

"""@pylatest
.. test_step:: 2

    Donec et mollis dolor::

        $ foo --extra sth
        $ bar -vvv
"""

"""@pylatest
.. test_result:: 2

    Maecenas congue ligula ac quam viverra nec
    consectetur ante hendrerit.
"""

"""@pylatest
.. test_step:: 3

    This one has no matching test result.
"""

"""@pylatest
.. test_result:: 4

    And this result has no test step.
"""

"""@pylatest
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
