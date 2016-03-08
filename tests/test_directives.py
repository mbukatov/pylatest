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


def testparse(rst_str):
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
    document = docutils.utils.new_document('testparse() method', settings)
    # parsing
    rst_parser.parse(rst_str, document)
    return document.pformat()


class TestDirectivesBase(unittest.TestCase):

    def setUp(self):
        # register custom pylatest nodes with html translator
        pylatest.xdocutils.client.register_plain()
        # show full diff (note: python3 unittest diff is much better)
        self.maxDiff = None

    def check_directive(self, rst_input, exp_result):
        result = testparse(rst_input)
        self.assertEqual(result, exp_result)


class TestDirectives(TestDirectivesBase):
    """
    Make sure that docutils isn't broken.
    """

    def test_docutils_works_fine_empty(self):
        rst_input = ""
        exp_result = '<document source="testparse() method">\n'
        self.check_directive(rst_input, exp_result)

    def test_docutils_works_fine_somedirective(self):
        rst_input = textwrap.dedent('''\
        .. container::

            Lorem ipsum.
        ''')
        exp_result = textwrap.dedent('''\
        <document source="testparse() method">
            <container>
                <paragraph>
                    Lorem ipsum.
        ''')
        self.check_directive(rst_input, exp_result)


class TestTestMetadataDirective(TestDirectivesBase):

    def test_testmetadata_empty(self):
        rst_input = '.. test_metadata:: author'
        exp_result = textwrap.dedent('''\
        <document source="testparse() method">
            <system_message level="3" line="1" source="testparse() method" type="ERROR">
                <paragraph>
                    Error in "test_metadata" directive:
                    2 argument(s) required, 1 supplied.
                <literal_block xml:space="preserve">
                    .. test_metadata:: author
        ''')
        self.check_directive(rst_input, exp_result)

    def test_testmetadata_single(self):
        rst_input = '.. test_metadata:: author foo@example.com'
        exp_result = textwrap.dedent('''\
        <document source="testparse() method">
            <pending>
                .. internal attributes:
                     .transform: pylatest.xdocutils.transforms.TestMetadataPlainTransform
                     .details:
                       meta_name: 'author'
                       meta_value: 'foo@example.com'
        ''')
        self.check_directive(rst_input, exp_result)

    def test_testmetadata_two_authors(self):
        rst_input = '.. test_metadata:: author foo@example.com bar@example.com'
        exp_result = textwrap.dedent('''\
        <document source="testparse() method">
            <pending>
                .. internal attributes:
                     .transform: pylatest.xdocutils.transforms.TestMetadataPlainTransform
                     .details:
                       meta_name: 'author'
                       meta_value: 'foo@example.com bar@example.com'
        ''')
        self.check_directive(rst_input, exp_result)

    def test_testmetadata_multiple(self):
        rst_input = textwrap.dedent('''\
        .. test_metadata:: author foo@example.com
        .. test_metadata:: date 2015-11-06
        .. test_metadata:: comment This is here just to test arg processing.
        ''')
        exp_result = textwrap.dedent('''\
        <document source="testparse() method">
            <pending>
                .. internal attributes:
                     .transform: pylatest.xdocutils.transforms.TestMetadataPlainTransform
                     .details:
                       meta_name: 'author'
                       meta_value: 'foo@example.com'
            <pending>
                .. internal attributes:
                     .transform: pylatest.xdocutils.transforms.TestMetadataPlainTransform
                     .details:
                       meta_name: 'date'
                       meta_value: '2015-11-06'
            <pending>
                .. internal attributes:
                     .transform: pylatest.xdocutils.transforms.TestMetadataPlainTransform
                     .details:
                       meta_name: 'comment'
                       meta_value: 'This is here just to test arg processing.'
        ''')
        self.check_directive(rst_input, exp_result)


class TestRequirementPlainDirective(TestDirectivesBase):

    def test_testmetadata_empty(self):
        rst_input = textwrap.dedent('''\
        .. requirement:: SOME_ID

            Some content.
        ''')
        exp_result = textwrap.dedent('''\
        <document source="testparse() method">
            <requirement_node>
                <paragraph>
                    Some content.
        ''')
        self.check_directive(rst_input, exp_result)
