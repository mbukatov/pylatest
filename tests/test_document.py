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

    def test_plainhtml_id(self):
        s1 = Section("Description")
        self.assertEqual(s1.html_id, "description")

    def test_get_rst_header(self):
        s1 = Section("Test Case Description")
        exp_output = textwrap.dedent('''\
        Test Case Description
        =====================''')
        self.assertEqual(s1.get_rst_header(), exp_output)
