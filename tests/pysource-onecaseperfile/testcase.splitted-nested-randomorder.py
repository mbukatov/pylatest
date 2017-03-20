#!/usr/bin/env python3
# -*- coding: utf8 -*-


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


import sys


def foobar():
    """@pylatest
    .. test_step:: 1

        List files in the volume: ``ls -a /mnt/helloworld``
    """
    print("here will be some code")
    print("here will be some code")
    print("here will be some code")

    """@pylatest
    .. test_result:: 1

        There are no files, output should be empty.
    """
    print("here will be some code")
    print("here will be some code")
    print("here will be some code")

def teardown():
    """
    Setup docstring.
    """
    print("here will be some code")
    print("here will be some code")
    print("here will be some code")
    """@pylatest
    Teardown
    ========

    #. Lorem ipsum dolor sit amet: ``rm -rf /mnt/helloworld``.

    #. Umount and remove ``lv_helloword`` volume.

    #. The end.
    """
    print("here will be some code")

def setup():
    """@pylatest
    Setup
    =====

    #. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec a diam
       lectus. Sed sit amet ipsum mauris.

    #. Use lvm disk paritioning and Leave 10G free space in volume
       called ``lv_helloword``.

    #. When the system is installed, format ``lv_helloword`` volume with
       brtfs using ``--super --special --options``.

    #. Mount it on a client::

        # mount -t btrfs /dev/mapper/vg_fedora/lv_helloword /mnt/helloworld

    #. Ceterum censeo, lorem ipsum::

        # dnf install foobar
        # systemctl enable foobard
    """
    print("here will be some code")
    print("here will be some code")
    print("here will be some code")

def test():
    """
    Test docstring.
    """
    foobar()

    """@pylatest
    .. test_step:: 2

        Donec et mollis dolor::

            $ foo --extra sth
            $ bar -vvv
    """
    print("here will be some code")
    print("here will be some code")
    print("here will be some code")

    """@pylatest
    .. test_result:: 2

        Maecenas congue ligula ac quam viverra nec
        consectetur ante hendrerit.
    """
    print("here will be some code")
    print("here will be some code")
    print("here will be some code")

    """@pylatest
    .. test_step:: 3

        This one has no matching test result.

    .. test_result:: 4

        And this result has no test step.
    """
    print("here will be some code")
    print("here will be some code")
    print("here will be some code")

def main():
    """@pylatest
    Hello World Test Case
    *********************

    :author: foo@example.com
    :date: 2015-11-06
    :comment: This is here just to test metadata processing.
    """
    setup()
    test()
    teardown()

if __name__ == '__main__':
    sys.exit(main())
