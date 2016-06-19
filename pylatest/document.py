# -*- coding: utf8 -*-

"""
Pylatest test case document module.

This module contains information about expected structure of pylatest document
types (eg. list of section titles) and other general functions.
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
    A section in pylatest reStructuredText document.
    """

    def __init__(self, title, html_id=True):
        self.title = title
        if html_id:
            self.html_id = title.lower()
        else:
            self.html_id = None

    def __eq__(self, other):
        return self.title == other.title

    def __hash__(self):
        return hash(self.title)

    def __str__(self):
        return "Section {0}".format(self.title)

    def get_rst_header(self):
        """
        Generate rst header code for this section.
        """
        return str(self.title) + '\n' + ('=' * len(self.title))


class TestCaseDoc(object):
    """
    Pylatest test case document.
    """

    DESCR = Section("Description")
    SETUP = Section("Setup")
    STEPS = Section("Test Steps", html_id=False)
    TEARD = Section("Teardown")
    _HEAD = Section("__header__", html_id=False)
    """
    Header pseudo section. It's not a real section, but a placeholder for data
    which includes:

     * main headline with a name of the test case
     * pylatest metadata directives

    Since this data can't be placed into a dedicated section (for obvious
    reasons: it's a main headline and immediate content with metadata), this
    header placeholder is not direcly included in ``SECTIONS`` tuple.
    """

    SECTIONS = [DESCR, SETUP, STEPS, TEARD]
    """
    List of sections expected in pylatest document (order matters).
    """

    SECTIONS_ALL = [_HEAD] + SECTIONS
    """
    List of titles of all sections in pylatest document (order matters),
    including HEADER pseudo section.
    """

    # TODO: remove during further refactoring?
    SECTIONS_PLAINHTML = [s.html_id for s in SECTIONS if s.html_id is not None]
    """
    List of ids of expected sections in plainhtml export of pylatest document.
    """

    @classmethod
    def has_section(cls, title):
        """
        Check if given title matches some section of pylatest test case
        document.
        """
        for section in cls.SECTIONS:
            if section.title == title:
                return True
        return False


# TODO: remove during merge

"""
List of action_name items of all pylatest actions.

*Pylatest action* is couple of test step and result with the same *action id*.

note: htmlplain div element uses just 'step' and 'result' - TODO: refactor?
"""
ACTION_NAMES = ("test_step", "test_result")
