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


import sys
import textwrap
import unittest

import docutils.frontend
import docutils.parsers.rst
import docutils.utils

import pylatest.xdocutils.directives
import pylatest.xdocutils.client


def _testparse(rst_str):
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


class TestBasePlain(unittest.TestCase):

    def setUp(self):
        # register custom pylatest nodes with html translator
        pylatest.xdocutils.client.register_plain()
        # show full diff (note: python3 unittest diff is much better)
        self.maxDiff = None

    def check_directive(self, rst_input, exp_result):
        result = _testparse(rst_input)
        assert result == exp_result


class TestDocutilsPlain(TestBasePlain):
    """
    Make sure that docutils isn't broken.
    """

    def test_docutils_works_fine_empty(self):
        rst_input = ""
        exp_result = '<document source="_testparse() method">\n'
        self.check_directive(rst_input, exp_result)

    def test_docutils_works_fine_somedirective(self):
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
        self.check_directive(rst_input, exp_result)


class TestTestActionsDirectivePlain(TestBasePlain):

    def test_teststep_empty(self):
        rst_input = '.. test_step:: 1'
        exp_result = textwrap.dedent('''\
        <document source="_testparse() method">
            <test_action_node action_id="1" action_name="test_step">
        ''')
        self.check_directive(rst_input, exp_result)

    def test_teststep_empty_noid(self):
        rst_input = '.. test_step::'
        exp_result = textwrap.dedent('''\
        <document source="_testparse() method">
            <system_message level="3" line="1" source="_testparse() method" type="ERROR">
                <paragraph>
                    Error in "test_step" directive:
                    1 argument(s) required, 0 supplied.
                <literal_block xml:space="preserve">
                    .. test_step::
        ''')
        self.check_directive(rst_input, exp_result)

    def test_testresult_empty(self):
        rst_input = '.. test_result:: 1'
        exp_result = textwrap.dedent('''\
        <document source="_testparse() method">
            <test_action_node action_id="1" action_name="test_result">
        ''')
        self.check_directive(rst_input, exp_result)

    def test_teststep_simple(self):
        rst_input = textwrap.dedent('''\
        .. test_step:: 7

            Some content.
        ''')
        exp_result = textwrap.dedent('''\
        <document source="_testparse() method">
            <test_action_node action_id="7" action_name="test_step">
                <paragraph>
                    Some content.
        ''')
        self.check_directive(rst_input, exp_result)

    def test_testresult_simple(self):
        rst_input = textwrap.dedent('''\
        .. test_result:: 7

            Some content.
        ''')
        exp_result = textwrap.dedent('''\
        <document source="_testparse() method">
            <test_action_node action_id="7" action_name="test_result">
                <paragraph>
                    Some content.
        ''')
        self.check_directive(rst_input, exp_result)


class TestRequirementDirectivePlain(TestBasePlain):

    def test_testmetadata_full_nooptions(self):
        rst_input = textwrap.dedent('''\
        .. requirement:: SOME_ID

            Some content.
        ''')
        exp_result = textwrap.dedent('''\
        <document source="_testparse() method">
            <requirement_node req_id="SOME_ID">
                <paragraph>
                    Some content.
        ''')
        self.check_directive(rst_input, exp_result)

    def test_testmetadata_full_alloptions(self):
        rst_input = textwrap.dedent('''\
        .. requirement:: FOO123
            :priority: high

            Natus illum repudiandae consequatur.

            Expedita saepe architecto numquam accusamus.
        ''')
        exp_result = textwrap.dedent('''\
        <document source="_testparse() method">
            <requirement_node priority="high" req_id="FOO123">
                <paragraph>
                    Natus illum repudiandae consequatur.
                <paragraph>
                    Expedita saepe architecto numquam accusamus.
        ''')
        self.check_directive(rst_input, exp_result)


class TestRequirementDirectiveTable(TestBasePlain):

    def setUp(self):
        # register custom pylatest nodes with html translator
        pylatest.xdocutils.client.register_table()
        # show full diff (note: python3 unittest diff is much better)
        self.maxDiff = None

    def test_testmetadata_full_nooptions(self):
        rst_input = textwrap.dedent('''\
        .. requirement:: SOME_ID

            Some content.
        ''')
        exp_result = textwrap.dedent('''\
        <document source="_testparse() method">
            <section ids="requirement-some-id" names="requirement\ some_id">
                <title>
                    Requirement SOME_ID
                <paragraph>
                    Some content.
        ''')
        self.check_directive(rst_input, exp_result)

    def test_testmetadata_full_alloptions(self):
        rst_input = textwrap.dedent('''\
        .. requirement:: FOO123
            :priority: high

            Natus illum repudiandae consequatur.

            Expedita saepe architecto numquam accusamus.
        ''')
        exp_result = textwrap.dedent('''\
        <document source="_testparse() method">
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
        self.check_directive(rst_input, exp_result)
