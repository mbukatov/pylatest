Just Another Test Case
**********************

:author: foo.bar@example.com

Description
===========

Vivamus fermentum semper porta. Nunc diam velit, adipiscing ut tristique
vitae, sagittis vel odio. Maecenas convallis ullamcorper ultricies.
Curabitur ornare, ligula semper consectetur sagittis, nisi diam iaculis
velit, id fringilla sem nunc vel mi. Nam dictum, odio nec pretium volutpat,
arcu ante placerat erat, non tristique elit urna et turpis.

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

.. test_step:: 1

    Suspendisse lectus leo, consectetur in tempor sit amet:

      * ``/var/log/messages``
      * ``/var/tmp``

.. test_result:: 1

    Suspendisse lectus leo, consectetur in tempor sit amet:

    #. Curabitur lobortis nisl a enim congue semper.

    #. Mauris ut placerat justo.

.. test_step:: 2

    Class aptent taciti sociosqu ad litora torquent per conubia nostra, per
    inceptos himenaeos.

.. test_result:: 2

    Hic sunt leones.

Teardown
========

#. Just: ``rm -rf /``.

#. The end.
