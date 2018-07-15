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


import re
import sys
import textwrap

import docutils.frontend
import docutils.parsers.rst
import docutils.utils
import pytest

import pylatest.xdocutils.directives
import pylatest.xdocutils.core


def _parse(rst_str):
    """
    Parse given string with rst parser, returns pformat string result.
    """
    # setup, see `docutils.utils.new_document()` or `docutils.parsers.rst`
    # docstrings for details
    rst_parser = docutils.parsers.rst.Parser()
    opt_parser = docutils.frontend.OptionParser(
        components=(docutils.parsers.rst.Parser,))
    settings = opt_parser.get_default_values()
    # setup: disable docutils error messages
    settings.report_level = 5
    settings.halt_level = 5
    document = docutils.utils.new_document('_testparse() method', settings)
    # parsing
    rst_parser.parse(rst_str, document)
    return document.pformat()


@pytest.fixture
def register_all_plain(scope="module"):
    """
    Register pylatest docutils extensions (nodes, directives ... but no
    transforms).
    """
    pylatest.xdocutils.core.register_all(use_plain=True)


def test_docutils_works_fine_empty(register_all_plain):
    rst_input = ""
    exp_result = '<document source="_testparse() method">\n'
    assert _parse(rst_input) == exp_result


def test_docutils_works_fine_somedirective(register_all_plain):
    rst_input = textwrap.dedent('''\
    .. container::

        Lorem ipsum.
    ''')
    exp_result = textwrap.dedent('''\
    <document source="_testparse() method">
        <container>
            <paragraph>
                Lorem ipsum.
    ''')
    assert _parse(rst_input) == exp_result


@pytest.mark.parametrize("action_id", [1, 23, 129])
@pytest.mark.parametrize("action_name", ["test_step", "test_result"])
def test_oldtestaction_empty(register_all_plain, action_id, action_name):
    rst_input = '.. {}:: {}'.format(action_name, action_id)
    exp_result = textwrap.dedent('''\
    <document source="_testparse() method">
        <test_action_node action_id="{}" action_name="{}">
    '''.format(action_id, action_name))
    assert _parse(rst_input) == exp_result


@pytest.mark.parametrize("action_name", ["test_step", "test_result"])
def test_oldtestaction_empty_noid(register_all_plain, action_name):
    rst_input = '.. {}::'.format(action_name)
    exp_result = textwrap.dedent('''\
    <document source="_testparse() method">
        <system_message level="3" line="1" source="_testparse() method" type="ERROR">
            <paragraph>
                Error in "{0}" directive:
                1 argument(s) required, 0 supplied.
            <literal_block xml:space="preserve">
                .. {0}::
    '''.format(action_name))
    assert _parse(rst_input) == exp_result


@pytest.mark.xfail(reason="https://gitlab.com/mbukatov/pylatest/issues/10")
@pytest.mark.parametrize("action_id", ["foo", None])
@pytest.mark.parametrize("action_name", ["test_step", "test_result"])
def test_oldtestaction_empty_wrongid(register_all_plain, action_id, action_name):
    rst_input = '.. {}:: {}'.format(action_name, action_id)
    exp_result = textwrap.dedent('''\
    <document source="_testparse() method">
        <test_action_node action_id="{}" action_name="{}">
    '''.format(action_id, action_name))
    assert _parse(rst_input) == exp_result


@pytest.mark.parametrize("action_name", ["test_step", "test_result"])
def test_oldtestaction_simple(register_all_plain, action_name):
    rst_input = textwrap.dedent('''\
    .. {}:: 7

        Some content.
    '''.format(action_name))
    exp_result = textwrap.dedent('''\
    <document source="_testparse() method">
        <test_action_node action_id="7" action_name="{}">
            <paragraph>
                Some content.
    '''.format(action_name))
    assert _parse(rst_input) == exp_result


@pytest.mark.parametrize("action_name", ["test_step", "test_result"])
def test_oldtestaction_paragraph(register_all_plain, action_name):
    rst_input = textwrap.dedent('''\
    .. {}:: 7

        Some content.

        Donec et mollis dolor::

            $ foo --extra sth
            $ bar -vvv
    '''.format(action_name))
    exp_result = textwrap.dedent('''\
    <document source="_testparse() method">
        <test_action_node action_id="7" action_name="{}">
            <paragraph>
                Some content.
            <paragraph>
                Donec et mollis dolor:
            <literal_block xml:space="preserve">
                $ foo --extra sth
                $ bar -vvv
    '''.format(action_name))
    assert _parse(rst_input) == exp_result


def test_testaction_empty(register_all_plain):
    rst_input = '.. test_action::'
    exp_result = textwrap.dedent('''\
    <document source="_testparse() method">
    ''')
    assert _parse(rst_input) == exp_result


# TODO: consider reporting error instead, see https://gitlab.com/mbukatov/pylatest/issues/10
def test_testaction_with_other_content(register_all_plain):
    rst_input = textwrap.dedent('''\
    .. test_action::

        Hello there.
    ''')
    exp_result = textwrap.dedent('''\
    <document source="_testparse() method">
    ''')
    assert _parse(rst_input) == exp_result


@pytest.mark.parametrize("action_name", ["test_step", "test_result"])
def test_testaction_single_valid_field_empty(register_all_plain, action_name):
    rst_input = textwrap.dedent('''\
    .. test_action::
       :{}:
    '''.format(action_name[5:]))
    exp_result = textwrap.dedent('''\
    <document source="_testparse() method">
        <test_action_node action_id="None" action_name="{}">
    '''.format(action_name))
    result = _parse(rst_input)
    result, num = re.subn('action_id="[0-9]+"', 'action_id="None"', result)
    assert num == 1
    assert result == exp_result


@pytest.mark.xfail(reason="https://gitlab.com/mbukatov/pylatest/issues/10")
@pytest.mark.parametrize("action_name", ["test_foo", "test_123"])
def test_testaction_single_invalid_field_empty(register_all_plain, action_name):
    rst_input = textwrap.dedent('''\
    .. test_action::
       :{}:
    '''.format(action_name[5:]))
    exp_result = textwrap.dedent('''\
    <document source="_testparse() method">
        TODO: there should be node with error message
    '''.format(action_name))
    assert _parse(rst_input) == exp_result


@pytest.mark.xfail(reason="https://gitlab.com/mbukatov/pylatest/issues/10")
@pytest.mark.parametrize("action_name", ["test_step", "test_result"])
def test_testaction_duplicated_field(register_all_plain, action_name):
    rst_input = textwrap.dedent('''\
    .. test_action::
       :{0}: First value.
       :{0}: And 2nd value.
    '''.format(action_name[5:]))
    exp_result = textwrap.dedent('''\
    <document source="_testparse() method">
        TODO: there should be node with clear error message
    '''.format(action_name))
    assert _parse(rst_input) == exp_result


@pytest.mark.parametrize("step_val", [
    " Wait about 20 minutes.",
    "\n           Wait about 20 minutes.\n",
    ])
@pytest.mark.parametrize("result_val", [
    " Nothing happens.",
    "\n           Nothing happens.\n",
    ])
def test_testaction_both_fields_simple(register_all_plain, step_val, result_val):
    rst_input = textwrap.dedent('''\
    .. test_action::
       :step:{}
       :result:{}
    '''.format(step_val, result_val))
    exp_result = textwrap.dedent('''\
    <document source="_testparse() method">
        <test_action_node action_id="None" action_name="test_step">
            <paragraph>
                Wait about 20 minutes.
        <test_action_node action_id="None" action_name="test_result">
            <paragraph>
                Nothing happens.
    ''')
    result = _parse(rst_input)
    result, num = re.subn('action_id="[0-9]+"', 'action_id="None"', result)
    assert num == 2
    assert result == exp_result


def test_testaction_both_fields_paragraph(register_all_plain):
    rst_input = textwrap.dedent('''\
    .. test_action::
       :step:
           List files in the volume: ``ls -a /mnt/helloworld`` ...

           and wait about 20 minutes.

       :result:
           Some content.

           Donec et mollis dolor::

               $ foo --extra sth
               $ bar -vvv
    ''')
    exp_result = textwrap.dedent('''\
    <document source="_testparse() method">
        <test_action_node action_id="None" action_name="test_step">
            <paragraph>
                List files in the volume: 
                <literal>
                    ls -a /mnt/helloworld
                 ...
            <paragraph>
                and wait about 20 minutes.
        <test_action_node action_id="None" action_name="test_result">
            <paragraph>
                Some content.
            <paragraph>
                Donec et mollis dolor:
            <literal_block xml:space="preserve">
                $ foo --extra sth
                $ bar -vvv
    ''')
    result = _parse(rst_input)
    result, num = re.subn('action_id="[0-9]+"', 'action_id="None"', result)
    assert num == 2
    assert result == exp_result


@pytest.mark.parametrize("action_name", ["test_step", "test_result"])
def test_testaction_single_valid_field_paragraph(register_all_plain, action_name):
    rst_input = textwrap.dedent('''\
    .. test_action::
       :{}:
           Some content.

           Donec et mollis dolor::

               $ foo --extra sth
               $ bar -vvv
    '''.format(action_name[5:]))
    exp_result = textwrap.dedent('''\
    <document source="_testparse() method">
        <test_action_node action_id="None" action_name="{}">
            <paragraph>
                Some content.
            <paragraph>
                Donec et mollis dolor:
            <literal_block xml:space="preserve">
                $ foo --extra sth
                $ bar -vvv
    '''.format(action_name))
    result = _parse(rst_input)
    result, num = re.subn('action_id="[0-9]+"', 'action_id="None"', result)
    assert num == 1
    assert result == exp_result
