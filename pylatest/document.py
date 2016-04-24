# -*- coding: utf8 -*-

"""
Pylatest test case document module.

This module contains information about expected structure (eg. list of section
titles) and TODO: other general functions.
"""

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


class Section(object):
    """
    A section in reStructuredText document.
    """

    def __init__(self, title, html_id=None):
        self.title = title
        # TODO: generate id from the title
        self.html_id = html_id


class TestActions(object):
    """
    List of action_name items of all pylatest actions.

    *Pylatest action* is couple of test step and result with the same *action id*.

    note: htmlplain div element uses just 'step' and 'result' - TODO: refactor?
    """
    ACTION_NAMES = ("test_step", "test_result")


class TestCaseDocument(object):
    """
    Pylatest test case document.
    """

    DESCR = Section("Description", "description")
    SETUP = Section("Setup", "setup")
    STEPS = Section("Test Steps")
    TEARD = Section("Teardown", "teardown")

    """
    Header pseudo section. It's not a real section, but a placeholder for data
    which includes:

     * main headline with a name of the test case
     * pylatest metadata directives

    Since this data can't be placed into a dedicated section (for obvious reasons:
    it's a main headline and immediate content with metadata), this header
    placeholder is not direcly included in ``SECTIONS`` tuple.
    """
    HEADER = Section("__header__")

    """
    List of sections expected in pylatest document (order matters).
    """
    sections = [DESCR, SETUP, STEPS, TEARD]

    """
    List of titles of all sections in pylatest document (order matters),
    including HEADER pseudo section.
    """
    sections_all = [HEADER] + SECTIONS


class RequirementItem(object):
    pass


class TestPlanDocument(object):
    pass
