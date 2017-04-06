# -*- coding: utf8 -*-

"""
Pylatest export module translates a test case description from a rst file into
xml document, which contains all metadata and docutils rendered html
representation of all sections of a test case document.
"""

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


from __future__ import print_function
import argparse

from lxml import etree

from pylatest.document import TestActions, TestCaseDoc
from pylatest.xdocutils.core import pylatest_plain_publish_parts


class XmlExportDoc(object):
    """
    Pylatest XML export format.
    """
    # TODO: fill the blanks, this is just an idea of how export may look like
    # TODO: proper design
    # TODO: add namespaces

    def __init__(self):
        """
        Generate empty skeleton of an export XML document.
        """
        self.xmltree = etree.Element('pylatest')
        self.metadata = etree.SubElement(self.xmltree, 'metadata')
        self.teststeps = etree.SubElement(self.xmltree, 'teststeps')

    def add_metadata(self, name, value):
        """
        Add metadata entry into xml export document.
        """
        # TODO

    def add_section(self, section, content):
        """
        Add pylatest section into xml export document.
        """
        section_el = etree.SubElement(self.xmltree, section)
        section_el.append(content)

    def add_action(self, action_id, action_name, content):
        """
        Add pylatest action into xml export document.
        """
        # TODO

    def tostring(self):
        """
        Generate a string representation of xml document.
        """
        return etree.tostring(self.xmltree)


def get_actions(tree):
    """
    Extracts pylatest actions from given html tree.
    """
    actions = TestActions()
    # check all pylatest action div elements
    for div_el in tree.xpath('//div[@class="pylatest_action"]'):
        action_id = int(div_el.get("action_id"))
        action_name = div_el.get("action_name")
        content = etree.tostring(div_el, method='html')
        actions.add(action_name, content, action_id)
    return actions

def get_section(tree, section_id):
    """
    Extracts given pylatest section from given html tree.
    """
    # selecting particular section via docutils div elements
    xpath = '//div[@class="section" and @id="{0}"]'.format(section_id)
    elem_list = tree.xpath(xpath)
    if len(elem_list) == 0:
        # this will effectivelly clean given section
        return None
    section = elem_list[0]
    # remove header element
    if section[0].tag.startswith('h'):
        del section[0]
    return section

def export_plainhtml(body_tree):
    """
    Translate given rst document into xml.
    """
    xml_export = XmlExportDoc()
    actions = get_actions(body_tree)
    for action_id, action_name, content in actions.iter_action():
        xml_export.add_action(action_id, action_name, content)
    for section in TestCaseDoc.SECTIONS_PLAINHTML:
        content = get_section(body_tree, section)
        if content is None:
            continue
        xml_export.add_section(section, content)
    # TODO: process test metadata, also use local configuration of defaults
    return xml_export

def rst2htmlbodytree(rst_content):
    """
    Translate given string which contains a content of rst file into processing
    friendly "pylatest plain html" xml tree.
    """
    parts = pylatest_plain_publish_parts(rst_content, writer_name='html')
    htmlbody_tree = etree.fromstring(parts['html_body'])
    return htmlbody_tree

def main():
    """
    Main method of ``pylatest-export`` command line tool.
    """
    parser = argparse.ArgumentParser(description='pylatest xml export tool')
    # TODO: automatic output xml filename based on input filename
    parser.add_argument(
        "rstfile",
        help="filename of testcase to be exported into xml form")
    args = parser.parse_args()

    # TODO: except IOError
    with open(args.rstfile, 'r') as src_file:
        rst_content = src_file.read()
        htmlbody_tree = rst2htmlbodytree(rst_content)
        xml_export = export_plainhtml(htmlbody_tree)
        print(xml_export.tostring())
