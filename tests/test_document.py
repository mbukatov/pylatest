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

import pylatest.document
from pylatest.document import SECTIONS, HEADER, SECTIONS_ALL


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
        self.actions.add(1, "test_step", "1.step")
        self.assertEqual(len(self.actions), 1)
        self.actions.add(1, "test_result", "1.result")
        self.assertEqual(len(self.actions), 1)
        self.assertEqual(
            list(self.actions.iter_content()), ["1.step", "1.result"])
        self.assertEqual(
            list(self.actions),
            [(1, '1.step', '1.result')])

    def test_actions_add_onestep(self):
        self.actions.add(1, "test_step", "1.step")
        self.assertEqual(len(self.actions), 1)
        self.assertEqual(
            list(self.actions.iter_content()), ["1.step"])
        self.assertEqual(
            list(self.actions),
            [(1, '1.step', None)])

    def test_actions_iter_twofull(self):
        self.actions.add(1, "test_step", "1.step")
        self.actions.add(1, "test_result", "1.result")
        self.actions.add(2, "test_step", "2.step")
        self.actions.add(2, "test_result", "2.result")
        self.assertEqual(
            list(self.actions),
            [(1, '1.step', '1.result'), (2, '2.step', '2.result')])


class TestSectionTuples(unittest.TestCase):
    """
    Test properties of SECTION and SECTION_ALL tuples.
    """

    def test_section_vs_sectionall_len(self):
        self.assertEqual(len(SECTIONS) + 1, len(SECTIONS_ALL))

    def test_header_membership(self):
        self.assertIn(HEADER, SECTIONS_ALL)
        self.assertNotIn(HEADER, SECTIONS)

    def test_sectionsall_contains_section(self):
        for section in SECTIONS:
            self.assertIn(section, SECTIONS_ALL)
