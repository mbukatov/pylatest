# -*- coding: utf8 -*-

"""
Pylatest test case document module.

**Pylatest document** means a description of a single test case written in rst
markup format.

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


"""
List of titles of expected sections in pylatest document (order matters).
"""
SECTIONS = (
    "Description",
    "Setup",
    "Test Steps",
    "Teardown")

"""
List of ids of expected sections in plainhtml export of pylatest document.
"""
SECTIONS_PLAINHTML = (
    "description",
    "setup",
    "teardown")

"""
List of action_name items of all pylatest actions.

*Pylatest action* is couple of test step and result with the same *action id*.

note: htmlplain div element uses just 'step' and 'result' - TODO: refactor?
"""
ACTION_NAMES = ("test_step", "test_result")

"""
Header pseudo section. It's not a real section, but a placeholder for data
which includes:

 * main headline with a name of the test case
 * pylatest metadata directives

Since this data can't be placed into a dedicated section (for obvious reasons:
it's a main headline and immediate content with metadata), this header
placeholder is not direcly included in ``SECTIONS`` tuple.
"""
HEADER = "__header__"

"""
List of titles of all sections in pylatest document (order matters),
including HEADER pseudo section.
"""
__tmp = [HEADER]
__tmp.extend(SECTIONS)
SECTIONS_ALL = tuple(__tmp)

# TODO: refactoring move actions processing here
