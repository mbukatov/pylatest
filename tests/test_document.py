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

    def test_actions_add_auto_id_value(self):
        auto_id = self.actions.add_step("1.step")
        self.assertEqual(auto_id, 1)
        auto_id = self.actions.add_step("2.step")
        self.assertEqual(auto_id, 2)
        auto_id = self.actions.add_result("2.result")
        self.assertEqual(auto_id, 2)
        auto_id = self.actions.add_result("3.result")
        self.assertEqual(auto_id, 3)
        auto_id = self.actions.add_step("3.step")
        self.assertEqual(auto_id, 3)

    def test_actions_iter_twofull_auto_id_firstonly(self):
        self.actions.add("test_step", "1.step", 1)
        self.actions.add("test_result", "1.result")
        self.actions.add("test_step", "2.step")
        self.actions.add("test_result", "2.result")
        self.assertEqual(
            list(self.actions),
            [(1, '1.step', '1.result'), (2, '2.step', '2.result')])


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
        =====================
        ''')
        self.assertEqual(s1.get_rst_header(), exp_output)


class TestTestCaseDoc(unittest.TestCase):
    """
    Test properties of TestCaseDoc class.
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
        tc.add_section(TestCaseDoc.DESCR, "string content", lineno=42)
        self.assertFalse(tc.is_empty())
        self.assertEqual(tc.sections, [TestCaseDoc.DESCR])
        self.assertEqual(
            sorted(tc.missing_sections + tc.sections),
            sorted(TestCaseDoc.SECTIONS_ALL))

    def test_rsttestcasedoc_add_section_multiple(self):
        tc = RstTestCaseDoc()
        tc.add_section(TestCaseDoc._HEAD, "header", lineno=42)
        tc.add_section(TestCaseDoc.DESCR, "description", lineno=83)
        self.assertFalse(tc.is_empty())
        self.assertEqual(
            sorted(tc.sections),
            sorted([TestCaseDoc._HEAD, TestCaseDoc.DESCR]))
        self.assertEqual(
            sorted(tc.missing_sections + tc.sections),
            sorted(TestCaseDoc.SECTIONS_ALL))

    def test_rsttestcasedoc_add_section_multiple_duplicit(self):
        tc = RstTestCaseDoc()
        tc.add_section(TestCaseDoc.DESCR, "descr. one", lineno=42)
        # 2nd value overrrides the original one
        tc.add_section(TestCaseDoc.DESCR, "descr. two", lineno=94)
        self.assertFalse(tc.is_empty())
        self.assertEqual(sorted(tc.sections), sorted([TestCaseDoc.DESCR]))
        self.assertEqual(
            sorted(tc.missing_sections + tc.sections),
            sorted(TestCaseDoc.SECTIONS_ALL))

    def test_rsttestcasedoc_add_section_few_multiple(self):
        tc = RstTestCaseDoc()
        tc.add_section(TestCaseDoc._HEAD, "header", lineno=10)
        tc.add_section(TestCaseDoc.DESCR, "description", lineno=55)
        tc.add_section(TestCaseDoc.SETUP, "setup", lineno=98)
        tc.add_section(TestCaseDoc.TEARD, "teardown", lineno=150)
        self.assertFalse(tc.is_empty())
        self.assertEqual(sorted(tc.sections), sorted([
            TestCaseDoc._HEAD,
            TestCaseDoc.DESCR,
            TestCaseDoc.SETUP,
            TestCaseDoc.TEARD]))
        self.assertEqual(tc.missing_sections, [TestCaseDoc.STEPS])
        self.assertEqual(
            sorted(tc.missing_sections + tc.sections),
            sorted(TestCaseDoc.SECTIONS_ALL))

    def test_rsttestcasedoc_add_testaction_wrong(self):
        tc = RstTestCaseDoc()
        with self.assertRaises(pylatest.document.PylatestActionsError):
            tc.add_test_action("test_foobarbaz", "content", 1)
        self.assertTrue(tc.is_empty())
        self.assertEqual(tc.sections, [])
        self.assertEqual(tc.missing_sections, TestCaseDoc.SECTIONS_ALL)
        self.assertEqual(
            sorted(tc.missing_sections + tc.sections),
            sorted(TestCaseDoc.SECTIONS_ALL))

    def test_rsttestcasedoc_add_testaction_simple(self):
        tc = RstTestCaseDoc()
        tc.add_test_action("test_step", "content", 1)
        self.assertFalse(tc.is_empty())
        self.assertEqual(tc.sections, [TestCaseDoc.STEPS])
        self.assertEqual(
            sorted(tc.missing_sections + tc.sections),
            sorted(TestCaseDoc.SECTIONS_ALL))

    def test_rsttestcasedoc_add_testaction_multiple(self):
        tc = RstTestCaseDoc()
        tc.add_test_action("test_step", "test step", 1)
        tc.add_test_action("test_result", "test result", 1)
        tc.add_test_action("test_step", "another test step", 2)
        self.assertFalse(tc.is_empty())
        self.assertEqual(tc.sections, [TestCaseDoc.STEPS])
        self.assertEqual(
            sorted(tc.missing_sections + tc.sections),
            sorted(TestCaseDoc.SECTIONS_ALL))

    def test_rsttestcasedoc_add_testaction_multiple_duplicit(self):
        tc = RstTestCaseDoc()
        tc.add_test_action("test_step", "test step", 1)
        with self.assertRaises(pylatest.document.PylatestActionsError):
            tc.add_test_action("test_step", "another test step", 1)
        self.assertFalse(tc.is_empty())
        self.assertEqual(tc.sections, [TestCaseDoc.STEPS])
        self.assertEqual(
            sorted(tc.missing_sections + tc.sections),
            sorted(TestCaseDoc.SECTIONS_ALL))


class TestRstTestCaseDocBuild(unittest.TestCase):

    def test_rsttestcasedoc_build_rst_empty(self):
        tc = RstTestCaseDoc()
        self.assertEqual(tc.build_rst(), "")

    def test_rsttestcasedoc_build_rst_onesection(self):
        tc = RstTestCaseDoc()
        content = textwrap.dedent('''\
        Description
        ===========

        This is just demonstration of usage of pylatest and
        expected structure of rst document.

        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec a diam
        lectus.  Sed sit amet ipsum mauris. Maecenas congue ligula ac quam
        viverra nec consectetur ante hendrerit. Donec et mollis dolor. Praesent
        et diam eget libero egestas mattis sit amet vitae augue.
        ''')
        tc.add_section(TestCaseDoc.DESCR, content, lineno=55)
        self.assertEqual(tc.build_rst(), content)

    def test_rsttestcasedoc_build_rst_onesection_header(self):
        tc = RstTestCaseDoc()
        content = textwrap.dedent('''\
        Hello World Test Case
        *********************

        .. test_metadata:: author foo@example.com
        .. test_metadata:: date 2015-11-06
        .. test_metadata:: comment Hello world.
        ''')
        tc.add_section(TestCaseDoc._HEAD, content, lineno=11)
        self.assertEqual(tc.build_rst(), content)

    def test_rsttestcasedoc_build_rst_multiple_sections(self):
        tc = RstTestCaseDoc()
        description = textwrap.dedent('''\
        Description
        ===========

        There is no Description.
        ''')
        setup = textwrap.dedent('''\
        Setup
        =====

        Lorem ipsum dolor sit amet, consectetur adipiscing elit.
        ''')
        expected_rst = textwrap.dedent('''\
        Description
        ===========

        There is no Description.

        Setup
        =====

        Lorem ipsum dolor sit amet, consectetur adipiscing elit.
        ''')
        tc.add_section(TestCaseDoc.SETUP, setup)
        tc.add_section(TestCaseDoc.DESCR, description)
        self.assertEqual(tc.build_rst(), expected_rst)

    def test_rsttestcasedoc_build_rst_single_action(self):
        tc = RstTestCaseDoc()
        step_1 = textwrap.dedent('''\
        .. test_step:: 1

            List files in the volume: ``ls -a /mnt/helloworld``
        ''')
        expected_rst = textwrap.dedent('''\
        Test Steps
        ==========

        .. test_step:: 1

            List files in the volume: ``ls -a /mnt/helloworld``
        ''')
        tc.add_test_action("test_step", step_1, 1)
        self.assertEqual(tc.build_rst(), expected_rst)

    def test_rsttestcasedoc_build_rst_single_action_single_section(self):
        tc = RstTestCaseDoc()
        step_1 = textwrap.dedent('''\
        .. test_step:: 1

            List files in the volume: ``ls -a /mnt/helloworld``
        ''')
        description = textwrap.dedent('''\
        Description
        ===========

        There is no Description.
        ''')
        expected_rst = textwrap.dedent('''\
        Description
        ===========

        There is no Description.

        Test Steps
        ==========

        .. test_step:: 1

            List files in the volume: ``ls -a /mnt/helloworld``
        ''')
        tc.add_test_action("test_step", step_1, 1)
        tc.add_section(TestCaseDoc.DESCR, description)
        self.assertEqual(tc.build_rst(), expected_rst)

    def test_rsttestcasedoc_build_rst_multiple_actions(self):
        tc = RstTestCaseDoc()
        step_1 = textwrap.dedent('''\
        .. test_step:: 1

            List files in the volume: ``ls -a /mnt/helloworld``
        ''')
        result_1 = textwrap.dedent('''\
        .. test_result:: 1

            There are no files, output should be empty.
        ''')
        step_2 = textwrap.dedent('''\
        .. test_step:: 2

            Donec et mollis dolor::

                $ foo --extra sth
                $ bar -vvv
        ''')
        expected_rst = textwrap.dedent('''\
        Test Steps
        ==========

        .. test_step:: 1

            List files in the volume: ``ls -a /mnt/helloworld``

        .. test_result:: 1

            There are no files, output should be empty.

        .. test_step:: 2

            Donec et mollis dolor::

                $ foo --extra sth
                $ bar -vvv
        ''')
        # call `add_test_action` in "random" order
        tc.add_test_action("test_step", step_2, 2)
        tc.add_test_action("test_result", result_1, 1)
        tc.add_test_action("test_step", step_1, 1)
        self.assertEqual(tc.build_rst(), expected_rst)

    def test_rsttestcasedoc_build_rst_multiple_actions_autoid(self):
        tc = RstTestCaseDoc()
        step_1 = textwrap.dedent('''\
        .. test_step::

            List files in the volume: ``ls -a /mnt/helloworld``
        ''')
        result_1 = textwrap.dedent('''\
        .. test_result::

            There are no files, output should be empty.
        ''')
        step_2 = textwrap.dedent('''\
        .. test_step::

            Donec et mollis dolor::

                $ foo --extra sth
                $ bar -vvv
        ''')
        expected_rst = textwrap.dedent('''\
        Test Steps
        ==========

        .. test_step::

            List files in the volume: ``ls -a /mnt/helloworld``

        .. test_result::

            There are no files, output should be empty.

        .. test_step::

            Donec et mollis dolor::

                $ foo --extra sth
                $ bar -vvv
        ''')
        # don't include action ids
        tc.add_test_action("test_step", step_1, None)
        tc.add_test_action("test_result", result_1, None)
        tc.add_test_action("test_step", step_2, None)
        self.assertEqual(tc.build_rst(), expected_rst)

    def test_rsttestcasedoc_build_rst_multiple_actions_with_section(self):
        """
        Note that when some test action directives are present, the actual
        content of test steps section is ignored (no matter what is there).
        """
        tc = RstTestCaseDoc()
        section_content = textwrap.dedent('''\
        Test Steps
        ==========

        .. test_step:: 1

            Here is the first step.

        .. test_result:: 1

            And the 2nd result.
        ''')
        step_2 = textwrap.dedent('''\
        .. test_step:: 2

            List files in the volume: ``ls -a /mnt/helloworld``
        ''')
        result_2 = textwrap.dedent('''\
        .. test_result:: 2

            There are no files, output should be empty.
        ''')
        step_3 = textwrap.dedent('''\
        .. test_step:: 3

            Donec et mollis dolor::

                $ foo --extra sth
                $ bar -vvv
        ''')
        expected_rst = textwrap.dedent('''\
        Test Steps
        ==========

        .. test_step:: 2

            List files in the volume: ``ls -a /mnt/helloworld``

        .. test_result:: 2

            There are no files, output should be empty.

        .. test_step:: 3

            Donec et mollis dolor::

                $ foo --extra sth
                $ bar -vvv
        ''')
        # call `add_test_action` in "random" order
        tc.add_test_action("test_step", step_3, 3)
        tc.add_test_action("test_result", result_2, 2)
        tc.add_test_action("test_step", step_2, 2)
        # and add test case section
        tc.add_section(TestCaseDoc.STEPS, section_content)
        self.assertEqual(tc.build_rst(), expected_rst)
