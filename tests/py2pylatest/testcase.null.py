#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""
Hello World Test Case
*********************

This is just demonstration of usage of pylatest rst directives and expected
structure of rst document.

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec a diam lectus.
Sed sit amet ipsum mauris. Maecenas congue ligula ac quam viverra nec
consectetur ante hendrerit. Donec et mollis dolor. Praesent et diam eget libero
egestas mattis sit amet vitae augue.

See :BZ:`439858` for more details.
"""


import sys


def setup():
    """
    Setup docstring.
    """
    print("here will be some code")
    print("here will be some code")
    print("here will be some code")
    """
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

def teardown():
    """
    Setup docstring.
    """
    print("here will be some code")
    print("here will be some code")
    print("here will be some code")
    """
    #. Lorem ipsum dolor sit amet: ``rm -rf /mnt/helloworld``.

    #. Umount and remove ``lv_helloword`` volume.

    #. The end.
    """
    print("here will be some code")


def test():
    """
    Test docstring.
    """
    print("here will be some code")
    print("here will be some code")
    print("here will be some code")

    """
        List files in the volume: ``ls -a /mnt/helloworld``
    """
    print("here will be some code")
    print("here will be some code")
    print("here will be some code")

    """
        There are no files, output should be empty.
    """
    print("here will be some code")
    print("here will be some code")
    print("here will be some code")

    """
        Donec et mollis dolor::

            $ foo --extra sth
            $ bar -vvv
    """
    print("here will be some code")
    print("here will be some code")
    print("here will be some code")

    """
        Maecenas congue ligula ac quam viverra nec
        consectetur ante hendrerit.
    """
    print("here will be some code")
    print("here will be some code")
    print("here will be some code")

    """
        This one has no matching test result.

        And this result has no test step.
    """
    print("here will be some code")
    print("here will be some code")
    print("here will be some code")

def main():
    """
    Main function of the test.
    """
    setup()
    test()
    teardown()

if __name__ == '__main__':
    sys.exit(main())
