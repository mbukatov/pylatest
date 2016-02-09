# -*- coding: utf8 -*-

"""
Pylatest test case document module.
"""

"""
List of headers of expected sections in pylatest document (order matters).
"""
SECTIONS = (
    "Description",
    "Setup",
    "Test Steps",
    "Teardown")

"""
Header section is not a real section, but a placeholder for data
which includes:

 * main headline with a name of the test case
 * pylatest metadata directives

Since this data can't be placed into a dedicated section (for obvious reasons:
it's a main headline and immediate content with metadata), this header
placeholder is not direcly included in ``SECTIONS`` tuple.
"""
HEADER = "__header__"

"""
List of headers of all sections in pylatest document (order matters),
including ``__header__`` data.
"""
__tmp = [HEADER]
__tmp.extend(SECTIONS)
SECTIONS_ALL = tuple(__tmp)

# TODO: refactoring move actions processing here
