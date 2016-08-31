# -*- coding: utf8 -*-

# Copyright (C) 2016 mbukatov@redhat.com
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


import unittest
import textwrap
import os

from pylatest.document import Section, TestCaseDoc, RstTestCaseDoc
import pylatest.document
import pylatest.xdocutils.client


class TestTestActions(unittest.TestCase):
    """
    Tests of pylatest.document.TestActions class.
    """

    def setUp(self):
        self.actions = pylatest.document.TestActions()

    def test_actions_null(self):
        self.assertEqual(len(self.actions), 0)

    def test_actions_iter_null(self):
        self.assertEqual(list(self.actions), [])
        self.assertEqual(list(self.actions.iter_content()), [])

    def test_actions_add_onefull(self):
        self.actions.add("test_step", "1.step", 1)
        self.assertEqual(len(self.actions), 1)
        self.actions.add("test_result", "1.result", 1)
        self.assertEqual(len(self.actions), 1)
        self.assertEqual(
            list(self.actions.iter_content()), ["1.step", "1.result"])
        self.assertEqual(
            list(self.actions),
            [(1, '1.step', '1.result')])

    def test_actions_add_error(self):
        with self.assertRaises(pylatest.document.PylatestActionsError):
            self.actions.add("test_foobar", "1.foobar", 1)
        self.assertEqual(len(self.actions), 0)

    def test_actions_add_onestep(self):
        self.actions.add("test_step", "1.step", 1)
        self.assertEqual(len(self.actions), 1)
        self.assertEqual(
            list(self.actions.iter_content()), ["1.step"])
        self.assertEqual(
            list(self.actions),
            [(1, '1.step', None)])

    def test_actions_add_oneresult(self):
        self.actions.add("test_result", "1.result", 1)
        self.assertEqual(len(self.actions), 1)
        self.assertEqual(
            list(self.actions.iter_content()), ["1.result"])
        self.assertEqual(
            list(self.actions),
            [(1, None, '1.result')])

    def test_actions_add_result(self):
        self.actions.add_result("1.result", 1)
        self.assertEqual(len(self.actions), 1)
        self.assertEqual(
            list(self.actions.iter_content()), ["1.result"])
        self.assertEqual(
            list(self.actions),
            [(1, None, '1.result')])

    def test_actions_add_step(self):
        self.actions.add_step("1.step", 1)
        self.assertEqual(len(self.actions), 1)
        self.assertEqual(
            list(self.actions.iter_content()), ["1.step"])
        self.assertEqual(
            list(self.actions),
            [(1, '1.step', None)])

    def test_actions_add_clash_enforce_id_false(self):
        self.actions = pylatest.document.TestActions(enforce_id=False)
        self.actions.add("test_step", "1.step-1", 1)
        self.actions.add("test_result", "1.result", 1)
        self.assertEqual(len(self.actions), 1)
        self.actions.add("test_step", "1.step-2", 1)
        self.assertEqual(len(self.actions), 1)
        self.assertEqual(
            list(self.actions.iter_content()), ["1.step-2", "1.result"])
        self.assertEqual(
            list(self.actions),
            [(1, '1.step-2', '1.result')])

    def test_actions_add_clash(self):
        self.actions.add("test_step", "1.step", 1)
        self.actions.add("test_result", "1.result", 1)
        self.assertEqual(len(self.actions), 1)
        with self.assertRaises(pylatest.document.PylatestActionsError):
            self.actions.add("test_step", "1.step-clash", 1)
        self.assertEqual(len(self.actions), 1)
        self.assertEqual(
            list(self.actions.iter_content()), ["1.step", "1.result"])
        self.assertEqual(
            list(self.actions),
            [(1, '1.step', '1.result')])

    def test_actions_iter_twofull(self):
        self.actions.add("test_step", "1.step", 1)
        self.actions.add("test_result", "1.result", 1)
        self.actions.add("test_step", "2.step", 2)
        self.actions.add("test_result", "2.result", 2)
        self.assertEqual(
            list(self.actions),
            [(1, '1.step', '1.result'), (2, '2.step', '2.result')])

    def test_actions_add_auto_id(self):
        self.actions.add_step("1.step")
        self.assertEqual(list(self.actions), [(1, '1.step', None)])
        self.actions.add_step("2.step")
        self.assertEqual(
            list(self.actions),
            [(1, '1.step', None), (2, '2.step', None)])
        self.actions.add_result("2.result")
        self.assertEqual(
            list(self.actions),
            [(1, '1.step', None), (2, '2.step', '2.result')])
        self.actions.add_result("3.result")
        self.assertEqual(list(self.actions), [
            (1, '1.step', None),
            (2, '2.step', '2.result'),
            (3, None, '3.result'), ])
        self.actions.add_step("3.step")
        self.assertEqual(list(self.actions), [
            (1, '1.step', None),
            (2, '2.step', '2.result'),
            (3, '3.step', '3.result'), ])

    def test_actions_iter_twofull_auto_id_firstonly(self):
        self.actions.add("test_step", "1.step", 1)
        self.actions.add("test_result", "1.result")
        self.actions.add("test_step", "2.step")
        self.actions.add("test_result", "2.result")
        self.assertEqual(
            list(self.actions),
            [(1, '1.step', '1.result'), (2, '2.step', '2.result')])


class TestTestCcaseDocSections(unittest.TestCase):
    """
    Test properties of SECTION and SECTION_ALL tuples.
    """

    def test_section_vs_sectionall_len(self):
        self.assertEqual(
            len(TestCaseDoc.SECTIONS) + 1,
            len(TestCaseDoc.SECTIONS_ALL))

    def test_header_membership(self):
        self.assertIn(TestCaseDoc._HEAD, TestCaseDoc.SECTIONS_ALL)
        self.assertNotIn(TestCaseDoc._HEAD, TestCaseDoc.SECTIONS)

    def test_sectionsall_contains_section(self):
        for section in TestCaseDoc.SECTIONS:
            self.assertIn(section, TestCaseDoc.SECTIONS_ALL)

    def test_has_section(self):
        self.assertTrue(TestCaseDoc.has_section(title="Description"))
        self.assertTrue(TestCaseDoc.has_section("Test Steps"))
        self.assertFalse(TestCaseDoc.has_section(title="Requirements"))
        self.assertFalse(TestCaseDoc.has_section("Foo Bar"))


class TestRstTestCaseDoc(unittest.TestCase):

    def test_rsttestcasedoc_empty(self):
        tc = RstTestCaseDoc()
        self.assertTrue(tc.is_empty())
        self.assertEqual(tc.sections, [])
        self.assertEqual(tc.missing_sections, TestCaseDoc.SECTIONS_ALL)

    def test_rsttestcasedoc_add_section_simple(self):
        tc = RstTestCaseDoc()
        tc.add_section("string content", 42, [TestCaseDoc.DESCR])
        self.assertFalse(tc.is_empty())
        self.assertEqual(tc.sections, [TestCaseDoc.DESCR])
        self.assertEqual(tc.missing_sections, [
            TestCaseDoc._HEAD,
            TestCaseDoc.SETUP,
            TestCaseDoc.STEPS,
            TestCaseDoc.TEARD])

    def test_rsttestcasedoc_add_section_multiple(self):
        tc = RstTestCaseDoc()
        tc.add_section("string content", 42, [TestCaseDoc._HEAD, TestCaseDoc.DESCR])
        self.assertFalse(tc.is_empty())
        self.assertEqual(sorted(tc.sections), sorted([TestCaseDoc._HEAD, TestCaseDoc.DESCR]))
        self.assertEqual(sorted(tc.missing_sections), sorted([
            TestCaseDoc.SETUP,
            TestCaseDoc.STEPS,
            TestCaseDoc.TEARD]))

    def test_rsttestcasedoc_add_section_few_multiple(self):
        tc = RstTestCaseDoc()
        tc.add_section("header and description", 10, [TestCaseDoc._HEAD, TestCaseDoc.DESCR])
        tc.add_section("setup", 42, [TestCaseDoc.SETUP])
        tc.add_section("teardown", 150, [TestCaseDoc.TEARD])
        self.assertFalse(tc.is_empty())
        self.assertEqual(sorted(tc.sections), sorted([
            TestCaseDoc._HEAD,
            TestCaseDoc.DESCR,
            TestCaseDoc.SETUP,
            TestCaseDoc.TEARD]))
        self.assertEqual(tc.missing_sections, [TestCaseDoc.STEPS])

    def test_rsttestcasedoc_add_testaction_simple(self):
        tc = RstTestCaseDoc()
        tc.add_test_action("test step", 10)
        self.assertFalse(tc.is_empty())
        self.assertEqual(tc.sections, [TestCaseDoc.STEPS])
        self.assertEqual(sorted(tc.missing_sections), sorted([
            TestCaseDoc._HEAD,
            TestCaseDoc.DESCR,
            TestCaseDoc.SETUP,
            TestCaseDoc.TEARD]))

    def test_rsttestcasedoc_add_testaction_multiple(self):
        tc = RstTestCaseDoc()
        tc.add_test_action("test step", 10)
        tc.add_test_action("test result", 12)
        tc.add_test_action("another test step", 20)
        self.assertFalse(tc.is_empty())
        self.assertEqual(tc.sections, [TestCaseDoc.STEPS])
        self.assertEqual(sorted(tc.missing_sections), sorted([
            TestCaseDoc._HEAD,
            TestCaseDoc.DESCR,
            TestCaseDoc.SETUP,
            TestCaseDoc.TEARD]))


class TestSection(unittest.TestCase):

    def test_sections_eq(self):
        s1 = Section("Test Steps")
        s2 = Section("Test Steps")
        s3 = Section("Requirements")
        self.assertEqual(s1, s2)
        self.assertNotEqual(s2, s3)
        self.assertNotEqual(s1, s3)

    def test_plainhtml_id(self):
        s1 = Section("Description")
        self.assertEqual(s1.html_id, "description")

    def test_get_rst_header(self):
        s1 = Section("Test Case Description")
        exp_output = textwrap.dedent('''\
        Test Case Description
        =====================''')
        self.assertEqual(s1.get_rst_header(), exp_output)


class TestPylatestDocstringProcessing(unittest.TestCase):
    """
    Test processing of pylatest docstrings.
    """

    def setUp(self):
        # commons steps required for all test cases
        pylatest.xdocutils.client.register_plain()

    def test_detect_docstring_sections_empty(self):
        self.assertEqual(pylatest.document.detect_docstring_sections(""), ([], 0))

    def test_detect_docstring_sections_nocontent(self):
        src = textwrap.dedent('''\
        Hello World Test Case
        *********************

        There are no pylatest data in this string.

        Test Stuff
        ==========

        Really, Hic sunt leones ...
        ''')
        self.assertEqual(pylatest.document.detect_docstring_sections(src), ([], 0))

    def test_detect_docstring_sections_header(self):
        src = textwrap.dedent('''\
        Hello World Test Case
        *********************

        .. test_metadata:: author foo@example.com
        .. test_metadata:: date 2015-11-06
        .. test_metadata:: comment Hello world.
        ''')
        expected_result = ([TestCaseDoc._HEAD], 0)
        actual_result = pylatest.document.detect_docstring_sections(src)
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
        actual_result = pylatest.document.detect_docstring_sections(src)
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
        actual_result = pylatest.document.detect_docstring_sections(src)
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
        actual_result = pylatest.document.detect_docstring_sections(src)
        self.assertEqual(actual_result, expected_result)

    def test_detect_docstring_sections_teststep_single(self):
        src = textwrap.dedent('''\
        .. test_step:: 1

            List files in the volume: ``ls -a /mnt/helloworld``
        ''')
        expected_result = ([], 1)
        actual_result = pylatest.document.detect_docstring_sections(src)
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
        actual_result = pylatest.document.detect_docstring_sections(src)
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
        actual_result = pylatest.document.detect_docstring_sections(src)
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
        actual_result = pylatest.document.detect_docstring_sections(src)
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
        actual_result = pylatest.document.detect_docstring_sections(src)
        actual_result = (sorted(actual_result[0]), actual_result[1])
        self.assertEqual(actual_result, expected_result)
