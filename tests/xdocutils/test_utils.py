# -*- coding: utf8 -*-

"""
Tests of helper functions from pylatest.xdocutils.utils module.
"""

# Copyright (C) 2018 Martin Bukatovič <martin.bukatovic@gmail.com>
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


import textwrap

from docutils.core import publish_doctree
import pytest

from pylatest.xdocutils.core import pylatest_publish_parts
from pylatest.xdocutils.readers import NoDocInfoReader
from pylatest.xdocutils.utils import get_field_list
from pylatest.xdocutils.utils import get_testcase_id


def _publish(source):
    """
    Parse rst source string into doctree.
    """
    doctree = publish_doctree(
        source=source,
        reader=NoDocInfoReader(),
        parser_name='restructuredtext',)
    return doctree


def test_get_field_list_null(empty_doctree):
    assert get_field_list(empty_doctree) == None


def test_get_field_list_missing():
    doctree = _publish(textwrap.dedent('''\
    Test Foo
    ********

    There is no field list.

    Description
    ===========

    Nothing here as well.
    '''))
    assert get_field_list(doctree) == None


def test_get_field_list_present():
    doctree = _publish(textwrap.dedent('''\
    Test Foo
    ********

    :id: FOO-122
    :author: joe.foo@example.com
    :component: foo
    '''))
    assert get_field_list(doctree) is not None


def test_get_testcase_id_null(empty_doctree):
    assert get_testcase_id(empty_doctree) == None


def test_get_testcase_id():
    doctree = _publish(textwrap.dedent('''\
    Test Foo
    ********

    :id: FOO-122
    :author: joe.foo@example.com
    :component: foo
    '''))
    assert get_testcase_id(doctree) == "FOO-122"
