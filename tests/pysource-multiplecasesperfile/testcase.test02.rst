Ahoj Světe Test Case
********************

:author: bar@example.com
:date: 2015-11-07

Description
===========

Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium
doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore
veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim
ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia
consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt.

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

    List files in the volume: ``ls -a /mnt/somethingelse``

.. test_result:: 1

    There are some files, output should not be empty.

.. test_step:: 2

    Donec et mollis dolor::

        $ foobar --sth
        $ find /mnt/somethingelse -name foo02 | wc -l

.. test_result:: 2

    Maecenas congue ligula ac quam viverra nec
    consectetur ante hendrerit.

Teardown
========

#. Lorem ipsum dolor sit amet: ``rm -rf /mnt/helloworld``.

#. Umount and remove ``lv_helloword`` volume.

#. The end.
