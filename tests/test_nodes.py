# -*- coding: utf8 -*-

# Copyright (C) 2016 martin.bukatovic@gmail.com
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
import unittest
import xml.etree.ElementTree as ET

from docutils import nodes
from docutils.core import publish_from_doctree, publish_doctree

import pylatest.client
import pylatest.nodes


class TestCustomNodes(unittest.TestCase):
    """
    Test custom pylatest nodes.
    """

    def setUp(self):
        # register custom pylatest nodes with html translator
        pylatest.client.register_pylatest_nodes()
        # produce empty document tree
        self.doctree = publish_doctree(
            source="",
            reader_name='standalone',
            parser_name='restructuredtext',)

    def _publish_pseudoxml(self):
        output = publish_from_doctree(
            self.doctree,
            settings_overrides={'output_encoding': 'unicode'},)
        return output

    def _publish_html(self):
        output = publish_from_doctree(
            self.doctree,
            writer_name='html',
            settings_overrides={
                # 'output_encoding': 'unicode',
                'stylesheet_path': None,
                })
        return output

    def test_pylatest_doesnt_break_docutils(self):
        output = self._publish_pseudoxml()
        self.assertEqual(output.strip(), '<document source="<string>">')

    def test_test_step_node(self):
        self.doctree += pylatest.nodes.test_step_node()
        output = self._publish_pseudoxml()
        exp_result = textwrap.dedent('''\
        <document source="<string>">
            <test_step_node>
        ''')
        self.assertEqual(output, exp_result)

    # TODO: add test cases for test_result_node and test_metadata_node

    def test_test_step_node_with_content_html(self):
        # create test step node with some content
        node = pylatest.nodes.test_step_node()
        node.attributes["action_id"] = 1
        node += nodes.paragraph(text="Just do something.")
        # add this node into doctree
        self.doctree += node
        # generate html into string
        output = self._publish_html()
        # search for pylatest action div element for this test_step_node
        output_tree = ET.fromstring(output)
        xml_ns = 'http://www.w3.org/1999/xhtml'
        node_xpath = ".//{{{0}}}body/{{{0}}}div[@class='pylatest_action']/"
        node_list = output_tree.findall(node_xpath.format(xml_ns))

        # TODO: fix this (the element is there, but it's not in the list)
        # self.assertEqual(len(node_list), 1)

        # examine the div element
        # node_el = node_list[0]
        # exp_result = textwrap.dedent('''\
        # ''')
        # self.assertEqual(output, exp_result)
