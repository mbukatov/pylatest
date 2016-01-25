#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""
Hello World Test Case
*********************

.. test_metadata:: author foo@example.com
.. test_metadata:: date 2015-11-06
.. test_metadata:: comment This is here just to test metadata processing.

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

Test Steps
==========

"""


import sys


def main():
    print("done")

if __name__ == '__main__':
    sys.exit(main())
