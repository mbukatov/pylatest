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
import xml.etree.ElementTree as ET

from docutils import nodes
from docutils.core import publish_from_doctree
import pytest

import pylatest.xdocutils.core
import pylatest.xdocutils.nodes


@pytest.fixture
def register_nodes(scope="module"):
    """
    Register custom pylatest nodes with html translator.
    """
    pylatest.xdocutils.core.register_pylatest_nodes()


def publish_pseudoxml(doctree):
    """
    Returns string with pseudo xml rendering of ``doctree``.
    """
    output = publish_from_doctree(
        doctree,
        settings_overrides={'output_encoding': 'unicode'},)
    return output


def publish_html(doctree):
    """
    Returns string with html rendering of ``doctree``.
    """
    output = publish_from_doctree(
        doctree,
        writer_name='html',
        settings_overrides={
            # 'output_encoding': 'unicode',
            'stylesheet_path': None,
            })
    return output


def test_pylatest_doesnt_break_docutils(empty_doctree):
    output = publish_pseudoxml(empty_doctree)
    assert output.strip() == '<document source="<string>">'


@pytest.mark.parametrize("node_name", pylatest.xdocutils.nodes.node_class_names)
def test_all_custom_nodes(empty_doctree, node_name):
    doctree = empty_doctree
    # create test step without any content
    node_class = getattr(pylatest.xdocutils.nodes, node_name)
    node = node_class()
    # add this node into doctree
    doctree += node
    # generate html into string
    output = publish_pseudoxml(doctree)
    # check the result
    exp_result = textwrap.dedent('''\
    <document source="<string>">
        <{0:s}>
    '''.format(node_name))
    assert output == exp_result


@pytest.mark.parametrize("action_name", ["test_step", "test_result"])
def test_action_node_with_content_html(empty_doctree, action_name, register_nodes):
    doctree = empty_doctree
    # create test step node with some content
    node = pylatest.xdocutils.nodes.test_action_node()
    node.attributes["action_id"] = 7
    node.attributes["action_name"] = action_name
    node += nodes.paragraph(text="Just do it!")
    # add this node into doctree
    doctree += node
    # generate html into string
    output = publish_html(doctree)
    # this test step node should be rendered as a div element
    # so search for pylatest action div elements in the output string
    output_tree = ET.fromstring(output)
    xml_ns = 'http://www.w3.org/1999/xhtml'
    node_xpath = ".//{%s}div[@class='pylatest_action']" % xml_ns
    node_list = output_tree.findall(node_xpath)
    # check that there is only one such node
    assert len(node_list) == 1
    # examine the div element
    node_el = node_list[0]
    assert node_el.text.strip() == "Just do it!"
    assert node_el.get("action_id") == "7"
    assert node_el.get("action_name") == action_name
