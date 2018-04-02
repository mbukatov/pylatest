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


import textwrap

from pylatest.xdocutils.core import pylatest_publish_parts


def _publish(rst_input):
    """
    Run docutils publisher with pylatest transforms enabled (done via custom
    option use_plain=False). Returns string with pseudoxml output.
    """
    result = pylatest_publish_parts(
        source=rst_input,
        writer_name='pseudoxml',
        use_plain=False)
    return result['whole']


def test_requirementsectiontransform_full_nooptions():
    rst_input = textwrap.dedent('''\
    .. requirement:: SOME_ID

        Some content.
    ''')
    exp_result = textwrap.dedent('''\
    <document source="<string>">
        <section ids="requirement-some-id" names="requirement\ some_id">
            <title>
                Requirement SOME_ID
            <paragraph>
                Some content.
    ''')
    assert _publish(rst_input) == exp_result


def test_requirementsectiontransform_full_alloptions():
    rst_input = textwrap.dedent('''\
    .. requirement:: FOO123
        :priority: high

        Natus illum repudiandae consequatur.

        Expedita saepe architecto numquam accusamus.
    ''')
    exp_result = textwrap.dedent('''\
    <document source="<string>">
        <section ids="requirement-foo123" names="requirement\ foo123">
            <title>
                Requirement FOO123
            <paragraph>
                Priority: high
            <paragraph>
                Natus illum repudiandae consequatur.
            <paragraph>
                Expedita saepe architecto numquam accusamus.
    ''')
    assert _publish(rst_input) == exp_result
