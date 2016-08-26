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

from pylatest.document import Section, TestCaseDoc
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


class TestSection(unittest.TestCase):

    def test_sections_eq(self):
        s1 = Section("Test Steps")
        s2 = Section("Test Steps")
        s3 = Section("Requirements")
        self.assertEqual(s1, s2)
        self.assertNotEqual(s2, s3)
        self.assertNotEqual(s1, s3)

    def test_sections_eq_withcontent(self):
        s1 = Section("Test Steps")
        s2 = Section("Test Steps")
        self.assertEqual(s1, s2)
        s1.content = "foo"
        self.assertNotEqual(s1, s2)
        s2.content = "foo"
        self.assertEqual(s1, s2)
        s2.content = "bar"
        self.assertNotEqual(s1, s2)

    def test_plainhtml_id(self):
        s1 = Section("Description")
        self.assertEqual(s1.html_id, "description")

    def test_get_rst_header(self):
        s1 = Section("Test Case Description")
        exp_output = textwrap.dedent('''\
        Test Case Description
        =====================''')
        self.assertEqual(s1.get_rst_header(), exp_output)

    def test_get_rst_content_empty(self):
        s1 = Section("Test Case Description")
        self.assertIsNone(s1.content)
        exp_output = textwrap.dedent('''\
        Test Case Description
        =====================''')
        self.assertEqual(s1.get_rst(), exp_output)

    def test_get_rst_content_simple(self):
        s1 = Section("Test Case Description")
        self.assertIsNone(s1.content)
        s1.content = "Hello World!"
        exp_output = textwrap.dedent('''\
        Test Case Description
        =====================

        Hello World!''')
        self.assertEqual(s1.get_rst(), exp_output)
