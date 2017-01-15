# -*- coding: utf8 -*-

# Copyright (C) 2017 Martin Bukatovič <martin.bukatovic@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


import os
import textwrap
import unittest

from pylatest.document import TestCaseDoc
import pylatest.rstsource as rstsource
import pylatest.xdocutils.client


class TestFindSections(unittest.TestCase):

    def setUp(self):
        # commons steps required for all test cases
        pylatest.xdocutils.client.register_plain()

    def test_find_sections_emptydoc(self):
        self.assertEqual(rstsource.find_sections(""), [])

    def test_find_sections_docwithoutsections_one(self):
        src = textwrap.dedent('''\
        Hello World
        ***********

        There are no sections, just a document title.
        ''')
        self.assertEqual(rstsource.find_sections(src), [])

    def test_find_sections_docwithoutsections_two(self):
        src = textwrap.dedent('''\
        =============
         Hello World
        =============

        Again, there are no sections, just a document title.
        ''')
        self.assertEqual(rstsource.find_sections(src), [])

    def test_find_sections_simpledoc(self):
        src = textwrap.dedent('''\
        Section One
        ***********

        Foo.

        Section Two
        ***********

        Bar.
        ''')
        exp_sections = [
            rstsource.RstSection("Section One", 1, 5),
            rstsource.RstSection("Section Two", 6, 9),
            ]
        self.assertEqual(rstsource.find_sections(src), exp_sections)


    def test_find_sections_multilevel(self):
        src = textwrap.dedent('''\
        ===============
         Status Report
        ===============

        Lieber ein Spatz in der Hand als eine Taube auf dem Dach.

        Header One
        ==========

        Here is some text.

        .. while this line tries to hide itself

        Achtung
        ```````

        In this piece of code, we can see a similar issue::

           def foo(bar):
               return False

        Header Two
        ==========

        And here we have some text again.

        Header Three
        ============
        ''')
        exp_sections = [
            rstsource.RstSection("Header One", 7, 21),
            rstsource.RstSection("Header Two", 22, 26),
            rstsource.RstSection("Header Three", 27, 28),
            ]
        self.assertEqual(rstsource.find_sections(src), exp_sections)

    def test_find_sections_multilevel_with_testmetadata(self):
        src = textwrap.dedent('''\
        =============
         Test FooBar
        =============

        .. test_metadata:: author foo@example.com
        .. test_metadata:: date 2015-11-06

        Header One
        ==========

        Here is some text.

        .. while this line tries to hide itself

        Achtung
        ```````

        In this piece of code, we can see a similar issue::

           def foo(bar):
               return False

        Header Two
        ==========

        And here we have some text again.

        Header Three
        ============
        ''')
        exp_sections = [
            rstsource.RstSection("Header One", 8, 22),
            rstsource.RstSection("Header Two", 23, 27),
            rstsource.RstSection("Header Three", 28, 29),
            ]
        self.assertEqual(rstsource.find_sections(src), exp_sections)

    def test_find_sections_multilevel_startswithline(self):
        src = textwrap.dedent('''\
        Having some text like this before any title will make this rst
        document to lack a title.

        ===============
         Status Report
        ===============

        Lieber ein Spatz in der Hand als eine Taube auf dem Dach.

        Header One
        ==========

        Here is some text.

        .. while this line tries to hide itself

        Achtung
        ```````

        In this piece of code, we can see a similar issue::

           def foo(bar):
               return False

        Header Two
        ==========

        And here we have some text again.
        ''')
        exp_sections = [
            rstsource.RstSection("Status Report", 5, 28),
            ]
        self.assertEqual(rstsource.find_sections(src), exp_sections)


class TestFindActions(unittest.TestCase):

    def setUp(self):
        # commons steps required for all test cases
        pylatest.xdocutils.client.register_plain()

    def test_find_actions_null(self):
        self.assertEqual(rstsource.find_actions(""), [])

    def test_find_actions_emptydoc(self):
        src = textwrap.dedent('''\
        Test Steps
        ==========

        There are no rst directives.
        ''')
        self.assertEqual(rstsource.find_actions(src), [])

    def test_find_actions_somedoc_noaction(self):
        src = textwrap.dedent('''\
        =============
         Test FooBar
        =============

        .. test_metadata:: author foo@example.com
        .. test_metadata:: date 2015-11-06

        Header One
        ==========

        Here is some text.

        .. while this line tries to hide itself

        Achtung
        ```````

        In this piece of code, we can see a similar issue::

           def foo(bar):
               return False

        Test Steps
        ==========

        There are no rst directives in this section.
        ''')
        self.assertEqual(rstsource.find_actions(src), [])

    def test_find_actions_somedoc_oneaction(self):
        src = textwrap.dedent('''\
        =============
         Test FooBar
        =============

        .. test_metadata:: author foo@example.com
        .. test_metadata:: date 2015-11-06

        Header One
        ==========

        Here is some text.

        .. while this line tries to hide itself

        Achtung
        ```````

        .. test_step:: 1

            Maecenas congue ligula ac quam viverra nec
            consectetur ante hendrerit.

        In this piece of code, we can see a similar issue::

           def foo(bar):
               return False

        Test Steps
        ==========

        There are no rst directives in this section.
        ''')
        exp_actions = [
            rstsource.RstTestAction(18, 22),
            ]
        self.assertEqual(rstsource.find_actions(src), exp_actions)

    def test_find_actions_real_looking_test_steps_section(self):
        src = textwrap.dedent('''\
        Test Steps
        ==========

        .. test_step:: 1

            list files in the volume: ``ls -a /mnt/helloworld``

        .. test_result:: 1

            there are no files, output should be empty.

        .. test_step:: 2

            donec et mollis dolor::

                $ foo --extra sth
                $ bar -vvv

        .. test_result:: 2

            Maecenas congue ligula ac quam viverra nec
            consectetur ante hendrerit.

        .. test_step:: 3

            This one has no matching test result.

        .. test_result:: 4

            And this result has no test step.

            Donec et mollis dolor::

                $ foo --extra sth
                $ bar -vvv

        .. test_step:: 5

            List files in the volume: ``ls -a /mnt/helloworld``

            This is the last step.
        ''')
        exp_actions = [
            rstsource.RstTestAction(4, 7),
            rstsource.RstTestAction(8, 11),
            rstsource.RstTestAction(12, 18),
            rstsource.RstTestAction(19, 23),
            rstsource.RstTestAction(24, 27),
            rstsource.RstTestAction(28, 36),
            rstsource.RstTestAction(37, 41),
            ]
        self.assertEqual(rstsource.find_actions(src), exp_actions)


class TestPylatestDocstringProcessing(unittest.TestCase):
    """
    Test processing of pylatest docstrings.
    """

    def setUp(self):
        # commons steps required for all test cases
        pylatest.xdocutils.client.register_plain()

    def test_detect_docstring_sections_empty(self):
        self.assertEqual(rstsource.detect_docstring_sections(""), ([], 0))

    def test_detect_docstring_sections_nocontent(self):
        src = textwrap.dedent('''\
        Hello World Test Case
        *********************

        There are no pylatest data in this string.

        Test Stuff
        ==========

        Really, Hic sunt leones ...
        ''')
        self.assertEqual(rstsource.detect_docstring_sections(src), ([], 0))

    def test_detect_docstring_sections_header(self):
        src = textwrap.dedent('''\
        Hello World Test Case
        *********************

        .. test_metadata:: author foo@example.com
        .. test_metadata:: date 2015-11-06
        .. test_metadata:: comment Hello world.
        ''')
        expected_result = ([TestCaseDoc._HEAD], 0)
        actual_result = rstsource.detect_docstring_sections(src)
        self.assertEqual(actual_result, expected_result)

    def test_detect_docstring_sections_description(self):
        src = textwrap.dedent('''\
        Description
        ===========

        This is just demonstration of usage of pylatest rst directives and
        expected structure of rst document.

        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec a diam
        lectus.  Sed sit amet ipsum mauris. Maecenas congue ligula ac quam
        viverra nec consectetur ante hendrerit. Donec et mollis dolor. Praesent
        et diam eget libero egestas mattis sit amet vitae augue.

        See :BZ:`439858` for more details.
        ''')
        expected_result = ([TestCaseDoc.DESCR], 0)
        actual_result = rstsource.detect_docstring_sections(src)
        self.assertEqual(actual_result, expected_result)

    def test_detect_docstring_sections_setup(self):
        src = textwrap.dedent('''\
        Setup
        =====

        #. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec a
           diam lectus. Sed sit amet ipsum mauris.

        #. Use lvm disk paritioning and Leave 10G free space in volume
           called ``lv_helloword``.

        #. When the system is installed, format ``lv_helloword`` volume with
           brtfs using ``--super --special --options``.

        #. Mount it on a client::

            # mount -t btrfs /dev/mapper/vg_fedora/lv_helloword /mnt/helloworld

        #. Ceterum censeo, lorem ipsum::

            # dnf install foobar
            # systemctl enable foobard
        ''')
        expected_result = ([TestCaseDoc.SETUP], 0)
        actual_result = rstsource.detect_docstring_sections(src)
        self.assertEqual(actual_result, expected_result)

    def test_detect_docstring_sections_teardown(self):
        src = textwrap.dedent('''\
        Teardown
        ========

        #. Lorem ipsum dolor sit amet: ``rm -rf /mnt/helloworld``.

        #. Umount and remove ``lv_helloword`` volume.

        #. The end.
        ''')
        expected_result = ([TestCaseDoc.TEARD], 0)
        actual_result = rstsource.detect_docstring_sections(src)
        self.assertEqual(actual_result, expected_result)

    def test_detect_docstring_sections_teststep_single(self):
        src = textwrap.dedent('''\
        .. test_step:: 1

            List files in the volume: ``ls -a /mnt/helloworld``
        ''')
        expected_result = ([], 1)
        actual_result = rstsource.detect_docstring_sections(src)
        self.assertEqual(actual_result, expected_result)

    def test_detect_docstring_sections_teststep_many(self):
        src = textwrap.dedent('''\
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

        .. test_step:: 5

            List files in the volume: ``ls -a /mnt/helloworld``
        ''')
        expected_result = ([], 7)
        actual_result = rstsource.detect_docstring_sections(src)
        self.assertEqual(actual_result, expected_result)

    def test_detect_docstring_sections_teststeps(self):
        src = textwrap.dedent('''\
        Test Steps
        ==========

        .. test_step:: 1

            List files in the volume: ``ls -a /mnt/helloworld``

        .. test_result:: 1

            There are no files, output should be empty.
        ''')
        expected_result = ([TestCaseDoc.STEPS], 2)
        actual_result = rstsource.detect_docstring_sections(src)
        self.assertEqual(actual_result, expected_result)

    def test_detect_docstring_sections_multi_header_teststeps(self):
        src = textwrap.dedent('''\
        Hello World Test Case
        *********************

        .. test_metadata:: author foo@example.com
        .. test_metadata:: date 2015-11-06

        Test Steps
        ==========

        .. test_step:: 1

            List files in the volume: ``ls -a /mnt/helloworld``

        .. test_result:: 1

            There are no files, output should be empty.
        ''')
        # note that order of sections is not defined
        expected_result = (sorted([TestCaseDoc._HEAD, TestCaseDoc.STEPS]), 2)
        actual_result = rstsource.detect_docstring_sections(src)
        actual_result = (sorted(actual_result[0]), actual_result[1])
        self.assertEqual(actual_result, expected_result)

    def test_detect_docstring_sections_multi_header_emptysteps_teardown(self):
        src = textwrap.dedent('''\
        Hello World Test Case
        *********************

        .. test_metadata:: author foo@example.com
        .. test_metadata:: date 2015-11-06

        Test Steps
        ==========

        There are no test steps!

        Teardown
        ========

        #. Lorem ipsum dolor sit amet: ``rm -rf /mnt/helloworld``.

        #. Umount and remove ``lv_helloword`` volume.

        #. The end.
        ''')
        # note that order of sections is not defined
        expected_sections = [TestCaseDoc._HEAD, TestCaseDoc.STEPS, TestCaseDoc.TEARD]
        expected_result = (sorted(expected_sections), 0)
        actual_result = rstsource.detect_docstring_sections(src)
        actual_result = (sorted(actual_result[0]), actual_result[1])
        self.assertEqual(actual_result, expected_result)
