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
from pylatest.xdocutils.utils import get_testcase_requirements


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


def test_get_testcase_requirements_null(empty_doctree):
    assert get_testcase_requirements(empty_doctree) == []


def test_get_testcase_requirements_single():
    doctree = _publish(textwrap.dedent('''\
    Test Foo
    ********

    :author: joe.foo@example.com
    :component: foo
    :requirement: FOO-212
    '''))
    assert get_testcase_requirements(doctree) == ["FOO-212"]


def test_get_testcase_requirements_single_emptyitem():
    doctree = _publish(textwrap.dedent('''\
    Test Foo
    ********

    :author: joe.foo@example.com
    :component: foo
    :requirement:
    '''))
    assert get_testcase_requirements(doctree) == []


def test_get_testcase_requirements_many():
    doctree = _publish(textwrap.dedent('''\
    Test Foo
    ********

    :author: joe.foo@example.com
    :requirement: FOO-212
    :requirement: FOO-232
    :component: foo
    '''))
    assert get_testcase_requirements(doctree) == ["FOO-212", "FOO-232"]


def test_get_testcase_requirements_single_list():
    doctree = _publish(textwrap.dedent('''\
    Test Foo
    ********

    :author: joe.foo@example.com
    :component: foo
    :requirements:
      - FOO-212
    '''))
    assert get_testcase_requirements(doctree) == ["FOO-212"]


def test_get_testcase_requirements_many_list():
    doctree = _publish(textwrap.dedent('''\
    Test Foo
    ********

    :author: joe.foo@example.com
    :component: foo
    :requirements:
      - FOO-212
      - FOO-232
    '''))
    assert get_testcase_requirements(doctree) == ["FOO-212", "FOO-232"]


def test_get_testcase_requirements_emptyitems_mixed_list():
    doctree = _publish(textwrap.dedent('''\
    Test Foo
    ********

    :author: joe.foo@example.com
    :component: foo
    :requirements:
      -
      - FOO-132
      -
    :requirement: FOO-130
    '''))
    assert get_testcase_requirements(doctree) == ["FOO-132", "FOO-130"]


def test_get_testcase_requirements_emptyitems_list():
    doctree = _publish(textwrap.dedent('''\
    Test Foo
    ********

    :author: joe.foo@example.com
    :component: foo
    :requirements:
      -
      -
    '''))
    assert get_testcase_requirements(doctree) == []


def test_get_testcase_requirements_many_list_err_single():
    doctree = _publish(textwrap.dedent('''\
    Test Foo
    ********

    :author: joe.foo@example.com
    :component: foo
    :requirements: FOO-212
    '''))
    assert get_testcase_requirements(doctree) == ["FOO-212"]


def test_get_testcase_requirements_many_mixed():
    doctree = _publish(textwrap.dedent('''\
    Test Foo
    ********

    :author: joe.foo@example.com
    :component: foo
    :requirement: FOO-012
    :requirement: FOO-032
    :requirements:
      - FOO-212
      - FOO-232
    '''))
    assert get_testcase_requirements(doctree) == [
        "FOO-012", "FOO-032", "FOO-212", "FOO-232"]


def test_get_testcase_requirements_single_url_link():
    doctree = _publish(textwrap.dedent('''\
    Test Foo
    ********

    :author: joe.foo@example.com
    :component: foo
    :requirement: https://example.com
    '''))
    results = get_testcase_requirements(doctree)
    assert len(results) == 1
    # check that we get actual rst node for a link (reference node)
    assert results[0].tagname == "reference"
    assert results[0].astext() == "https://example.com"


def test_get_testcase_requirements_many_list_url_link():
    doctree = _publish(textwrap.dedent('''\
    Test Foo
    ********

    :author: joe.foo@example.com
    :component: foo
    :requirements:
      - https://example.com/foo
      - https://example.com/bar
    '''))
    results = get_testcase_requirements(doctree)
    assert len(results) == 2
    # check that we get actual rst node for a link (reference node)
    assert results[0].tagname == "reference"
    assert results[1].tagname == "reference"
    # and expected content
    assert results[0].astext() == "https://example.com/foo"
    assert results[1].astext() == "https://example.com/bar"
