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

import pylatest.xdocutils.client
import pylatest.xdocutils.nodes


def get_empty_doctree():
    """
    Produce empty rst document tree.
    """
    doctree = publish_doctree(
        source="",
        reader_name='standalone',
        parser_name='restructuredtext',)
    return doctree


class TestCustomNodes(unittest.TestCase):
    """
    Test custom pylatest nodes.
    """

    def setUp(self):
        # register custom pylatest nodes with html translator
        pylatest.xdocutils.client.register_pylatest_nodes()
        # produce empty document tree
        self.doctree = get_empty_doctree()

    def _publish_pseudoxml(self):
        """
        Returns string with pseudo xml rendering of ``self.doctree``.
        """
        output = publish_from_doctree(
            self.doctree,
            settings_overrides={'output_encoding': 'unicode'},)
        return output

    def _publish_html(self):
        """
        Returns string with html rendering of ``self.doctree``.
        """
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

    def test_all_custom_nodes(self):
        for node_name in pylatest.xdocutils.nodes.node_class_names:
            # produce empty document tree
            self.doctree = get_empty_doctree()
            # create test step without any content
            node_class = getattr(pylatest.xdocutils.nodes, node_name)
            node = node_class()
            # add this node into doctree
            self.doctree += node
            # generate html into string
            output = self._publish_pseudoxml()
            # check the result
            exp_result = textwrap.dedent('''\
            <document source="<string>">
                <{0:s}>
            '''.format(node_name))
            self.assertEqual(output, exp_result)

    def test_test_step_node(self):
        # create test step without any content
        node = pylatest.xdocutils.nodes.test_step_node()
        # add this node into doctree
        self.doctree += node
        # generate html into string
        output = self._publish_pseudoxml()
        # check the result
        exp_result = textwrap.dedent('''\
        <document source="<string>">
            <test_step_node>
        ''')
        self.assertEqual(output, exp_result)

    def test_requirement_node(self):
        # create requirement without any content
        node = pylatest.xdocutils.nodes.requirement_node()
        # add this node into doctree
        self.doctree += node
        # generate html into string
        output = self._publish_pseudoxml()
        # check the result
        exp_result = textwrap.dedent('''\
        <document source="<string>">
            <requirement_node>
        ''')
        self.assertEqual(output, exp_result)

    # TODO: add test cases for test_result_node and test_metadata_node

    def test_test_step_node_with_content_html(self):
        # create test step node with some content
        node = pylatest.xdocutils.nodes.test_step_node()
        node.attributes["action_id"] = 7
        node += nodes.paragraph(text="Just do it!")
        # add this node into doctree
        self.doctree += node
        # generate html into string
        output = self._publish_html()
        # this test step node should be rendered as a div element
        # so search for pylatest action div elements in the output string
        output_tree = ET.fromstring(output)
        xml_ns = 'http://www.w3.org/1999/xhtml'
        node_xpath = ".//{%s}div[@class='pylatest_action']" % xml_ns
        node_list = output_tree.findall(node_xpath)
        # check that there is only one such node
        self.assertEqual(len(node_list), 1)
        # examine the div element
        node_el = node_list[0]
        self.assertEqual(node_el.text.strip(), "Just do it!")
        self.assertEqual(node_el.get("action_id"), "7")
        self.assertEqual(node_el.get("action_name"), "step")
