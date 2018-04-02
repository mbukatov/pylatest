#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""@pylatest
Hello World Test Case
*********************

:author: foo@example.com
:date: 2015-11-06
:comment: This is here just to test metadata processing.

Description
===========

This is just demonstration of usage of pylatest rst directives and expected
structure of rst document.

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec a diam lectus.
Sed sit amet ipsum mauris. Maecenas congue ligula ac quam viverra nec
consectetur ante hendrerit. Donec et mollis dolor. Praesent et diam eget libero
egestas mattis sit amet vitae augue.

See :RHBZ:`439858` for more details.

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
