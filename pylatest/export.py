# -*- coding: utf8 -*-

"""
Pylatest export module translates a test case description from a plain html
source string into XmlExportTestCaseDoc object, which contains all metadata and
docutils rendered html representation of all sections of a test case document.
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


from lxml import etree

from pylatest.document import XmlExportTestCaseDoc


# xml namespaces
NS = {'html': 'http://www.w3.org/1999/xhtml'}

# HTML namespace URI in lxml notation, see:
# http://lxml.de/tutorial.html#namespaces
HTML = "{%s}" % NS['html']


def get_actions(tree):
    """
    Extracts pylatest actions from given html tree.
    """
    actions = []
    for div_el in tree.xpath(
            '//html:div[@class="pylatest_action"]', namespaces=NS):
        action_id = int(div_el.get("action_id"))
        action_name = div_el.get("action_name")
        actions.append((action_id, action_name, div_el))
    return actions


def get_metadata(tree):
    """
    Extracts test case metadata from given html tree.
    """
    metadata = []
    # find all field lists in the tree
    fl_tables = tree.xpath(
        '//html:table[contains(@class, "field-list")]',
        namespaces=NS)
    if len(fl_tables) == 0:
        return metadata
    # we process only 1st field list we find, assuming it's the one with
    # metadata, we also assume that sphinx disables docinfo transform
    fl_el = fl_tables[0]
    for f_el in fl_el.xpath(
            '//html:tr[contains(@class, "field")]', namespaces=NS):
        name = f_el.xpath('./html:th[@class="field-name"]', namespaces=NS)[0]
        body = f_el.xpath('./html:td[@class="field-body"]', namespaces=NS)[0]
        # polish field name value, we expect that name element looks like this:
        # <th class="field-name">date:</th>
        name_value = name.text[:-1]
        # get body value
        body_tostr = etree.tostring(body, method="text")
        body_value = body_tostr.decode('utf-8').strip()
        metadata.append((name_value, body_value))
    return metadata


def get_section(tree, section_id):
    """
    Extracts given pylatest section from given html tree.
    """
    # selecting particular section via docutils div elements
    xpath = '//html:div[@class="section" and @id="{0}"]'.format(section_id)
    elem_list = tree.xpath(xpath, namespaces=NS)
    if len(elem_list) == 0:
        # this will effectivelly clean given section
        return None
    section = elem_list[0]
    # remove header element
    if section[0].tag.startswith(HTML + 'h'):
        del section[0]
    return section


def get_title(tree):
    """
    Extracts test case title from given html tree.
    """
    # we have to use h1 element, '/html:html/html:head/html:title' is empty
    el_list = tree.xpath('//html:h1', namespaces=NS)
    if len(el_list) == 0:
        return None
    # return text value of the element with title
    return el_list[0].text


def build_xml_testcase_doc(html_source, content_type=None, testcase_id=None):
    """
    Create xml export document (instance of XmlExportTestCaseDoc) for given
    test case html source string.
    """
    # return empty doc for empty input string
    if len(html_source) == 0:
        return XmlExportTestCaseDoc()

    html_tree = etree.fromstring(html_source.encode("utf8"))
    title = get_title(html_tree)
    doc = XmlExportTestCaseDoc(title, content_type, testcase_id)

    # extract metadata from html_tree
    for attr_name, content in get_metadata(html_tree):
        doc.add_metadata(attr_name, content)

    # extract sections from html_tree
    for section in XmlExportTestCaseDoc.SECTIONS:
        content = get_section(html_tree, section.html_id)
        if content is None:
            continue
        doc.add_section(section, content)

    # check all pylatest action div elements
    for action_id, action_name, el in get_actions(html_tree):
        doc.add_test_action(action_name, el, action_id)

    return doc


def add_properties(element, properties, prop_el_name):
    """
    Add ``properties`` (represented by ``prop_el_name`` elements) into given
    xml ``element``.
    """
    for name, value in properties.items():
        etree.SubElement(element, prop_el_name, attrib={
            'name': str(name),
            'value': str(value)})


def build_xml_export_doc(
        project_id=None,
        testcases=None,
        properties=None,
        response_properties=None):
    """
    Create xml export document for given testcases.
    """
    xml_tree = etree.Element('testcases')
    if project_id is not None:
        xml_tree.attrib["project-id"] = project_id
    if response_properties is not None and len(response_properties) > 0:
        resp_properties_el = etree.SubElement(xml_tree, 'response-properties')
        add_properties(
            resp_properties_el,
            response_properties,
            prop_el_name='response-property')
    if properties is not None and len(properties) > 0:
        properties_el = etree.SubElement(xml_tree, 'properties')
        add_properties(properties_el, properties, prop_el_name='property')
    if testcases is None:
        return xml_tree
    for tc in testcases:
        xml_tree.append(tc)
    return xml_tree
