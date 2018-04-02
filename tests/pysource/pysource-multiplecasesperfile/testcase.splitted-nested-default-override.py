#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""@pylatest test01
Hello World Test Case
*********************

:author: foo@example.com
:date: 2015-11-06
:comment: This is here just to test metadata processing.
"""

"""@pylatest default
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


def setup():
    """
    Setup docstring.
    """
    print("here will be some code")
    print("here will be some code")
    print("here will be some code")
    """@pylatest default
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

def teardown():
    """
    Setup docstring.
    """
    print("here will be some code")
    print("here will be some code")
    print("here will be some code")
    """@pylatest default
    Teardown
    ========

    #. Lorem ipsum dolor sit amet: ``rm -rf /mnt/helloworld``.

    #. Umount and remove ``lv_helloword`` volume.

    #. The end.
    """
    print("here will be some code")


def test01():
    """
    Test docstring.
    """
    print("here will be some code")
    print("here will be some code")
    print("here will be some code")

    """@pylatest test01
    .. test_step:: 1

        List files in the volume: ``ls -a /mnt/helloworld``
    """
    print("here will be some code")
    print("here will be some code")
    print("here will be some code")

    """@pylatest test01
    .. test_result:: 1

        There are no files, output should be empty.
    """
    print("here will be some code")
    print("here will be some code")
    print("here will be some code")

    """@pylatest test01
    .. test_step:: 2

        Donec et mollis dolor::

            $ foo --extra sth
            $ bar -vvv
    """
    print("here will be some code")
    print("here will be some code")
    print("here will be some code")

    """@pylatest test01
    .. test_result:: 2

        Maecenas congue ligula ac quam viverra nec
        consectetur ante hendrerit.
    """
    print("here will be some code")
    print("here will be some code")
    print("here will be some code")

    """@pylatest test01
    .. test_step:: 3

        This one has no matching test result.

    .. test_result:: 4

        And this result has no test step.
    """
    print("here will be some code")
    print("here will be some code")
    print("here will be some code")

def test02():
    """@pylatest test02
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
    """
    print("here will be some code")

    """@pylatest test02
    .. test_step:: 1

        List files in the volume: ``ls -a /mnt/somethingelse``
    """
    print("here will be some code")

    """@pylatest test02
    .. test_result:: 1

        There are some files, output should not be empty.
    """
    print("here will be some code")

    """@pylatest test02
    .. test_step:: 2

        Donec et mollis dolor::

            $ foobar --sth
            $ find /mnt/somethingelse -name foo02 | wc -l
    """
    print("here will be some code")

    """@pylatest test02
    .. test_result:: 2

        Maecenas congue ligula ac quam viverra nec
        consectetur ante hendrerit.
    """
    print("here will be some code")

def test03():
    """@pylatest test03
    .. test_step:: 1

        Suspendisse lectus leo, consectetur in tempor sit amet:

          * ``/var/log/messages``
          * ``/var/tmp``
    """
    print("here will be some code")

    """@pylatest test03
    .. test_result:: 1

        Suspendisse lectus leo, consectetur in tempor sit amet:

        #. Curabitur lobortis nisl a enim congue semper.

        #. Mauris ut placerat justo.
    """
    print("here will be some code")

    """@pylatest test03
    .. test_step:: 2

        Class aptent taciti sociosqu ad litora torquent per conubia nostra, per
        inceptos himenaeos.
    """
    print("here will be some code")

    """@pylatest test03
    .. test_result:: 2

        Hic sunt leones.
    """
    print("here will be some code")

def main():
    """
    Main function of the test.
    """
    setup()
    test01()
    teardown()

    setup()
    test02()
    teardown()

    """@pylatest test03
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
    """
    setup()
    test03()
    """@pylatest test03
    Teardown
    ========

    #. Just: ``rm -rf /``.

    #. The end.
    """
    print("here will be some code")


if __name__ == '__main__':
    sys.exit(main())
