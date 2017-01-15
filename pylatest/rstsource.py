# -*- coding: utf8 -*-

"""
Helper functions for processing of rst source text strings.
"""

# Copyright (C) 2017 Martin Bukatovič <martin.bukatovic@gmail.com>
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


import ast
import inspect
import os
import sys

from docutils.core import publish_doctree
from docutils import nodes

from pylatest.document import TestCaseDoc, Section
import pylatest.xdocutils.nodes


def _debug(nodetree):
    """
    Debug function for development purposes only.
    """
    print(nodetree.pformat())
    for node in nodetree.traverse():
        print("{}\t{}".format(node.line, node.tagname))


class RstSection(object):

    def __init__(self, title, start_line, end_line=None):
        self.title = title
        self.start_line = start_line
        self.end_line = end_line

    def __eq__(self, other):
        return self.title == other.title \
               and self.start_line == other.start_line \
               and self.end_line == other.end_line

    def __repr__(self):
        template = "RstSection('{}', {}, {})"
        return template.format(self.title, self.start_line, self.end_line)


class RstTestAction(object):

    def __init__(self, start_line, end_line=None):
        self.start_line = start_line
        self.end_line = end_line

    def __eq__(self, other):
        return self.start_line == other.start_line \
               and self.end_line == other.end_line

    def __repr__(self):
        template = "RstTestAction({}, {})"
        return template.format(self.start_line, self.end_line)


def get_last_line_num(str_value):
    """
    Returns 1-based line number (as used for text files) of the last line in
    given string.
    """
    if len(str_value) == 0:
        # special case: even empty string would be on the 1st line
        # when we ignore the rule about having '\n' in the end of *each* line
        return 1
    last_line = str_value.count('\n')
    # account for missing last '\n' character
    if str_value[-1] != "\n":
        last_line += 1
    return last_line


def find_sections(rst_source):
    """
    Finds all top level sections in given rst document.
    """
    # parse rst_source string to get rst node tree
    nodetree = publish_doctree(source=rst_source)
    sections = []
    prev_section = None
    for node in [n for n in nodetree.children if isinstance(n, nodes.section)]:
        title = node.children[0].astext()
        section = RstSection(title, node.line - 1)
        sections.append(section)
        if prev_section is not None:
            prev_section.end_line = node.line - 2
        prev_section = section
    # last section ends on the last line of the rst source
    if prev_section is not None:
        prev_section.end_line = get_last_line_num(rst_source)
    return sections


def _teststeps_condition(node):
    """
    Traverse condition for filtering nodes of test steps directives.
    """
    return (
        isinstance(node, pylatest.xdocutils.nodes.test_step_node) or
        isinstance(node, pylatest.xdocutils.nodes.test_result_node))


def _teststeps_condition_hack(node):
    """
    Traverse condition for filtering nodes of test steps directives.

    This is a quick hack to overcome issue with ``_teststeps_condition()``.
    """
    # TODO: proper check (of at least transformation class) goes here
    if isinstance(node, nodes.pending):
        return True
    return False


def find_actions(rst_source):
    # parse rst_source string to get rst node tree
    nodetree = publish_doctree(source=rst_source)

    actions = []
    for node in nodetree.traverse(_teststeps_condition):
        # we can't get line of the directive node directly, because docutils
        # doesn't provide it (node.line is None), but we can use the fact that
        # a paragraph node (which contains content of the directive) has line
        # attribute initialized properly
        #
        # pseudoxml tree of directive node looks like this:
        #
        # <test_result_node action_id="1">   # no line value for this node
        #     <paragraph>                    # we have line value here
        #         There are no files, output should be empty.
        start_line = node.children[0].line - 2
        # to get end line of a content of the directive node, we have to do
        # another hack (docutils node objects doesn't contain any information
        # about end line ) - we use next sibling node as a hint
        next_siblings = node.traverse(
            include_self=False,
            descend=False,
            siblings=True,
            )
        if len(next_siblings) > 0:
            next_node = next_siblings[0]
            # TODO: what if the next_node is not another directive?
            end_line = next_node.children[0].line - 3
        else:
            # when there are no next sibling nodes (this is the last directive
            # node in given subtree), we need to get to go up in the node tree
            # to get to the next node
            following_nodes = node.traverse(
                include_self=False,
                descend=False,
                ascend=True,
                siblings=False,
                )
            if len(following_nodes) > 0:
                # there are other nodes in the document tree after this node,
                # but on the higher level, see this example:
                #
                # <paragraph>
                #     <test_step_node action_id="1">
                #         <paragraph>
                #             Maecenas congue ligula ac quam viverra nec
                #             consectetur ante hendrerit.
                #         <paragraph>
                #             And that's all!
                # <paragraph>
                #     There is some other text after the directive.
                next_node = following_nodes[0]
                # type of next node needs to be considered to give corrent
                # end line number
                if next_node.tagname == "section":
                    end_line = next_node.line - 2
                else:
                    end_line = next_node.line - 1
            else:
                # ok, it seems this node is the last one in the rst source
                end_line = get_last_line_num(rst_source)
        # TODO: extract mode info about the node, eg. type (is it result or
        # step?) and pylatest id
        actions.append(RstTestAction(start_line, end_line))
    return actions


# TODO: this function will be deprecated, but let it here for now (reference
# and testing purposes)
def detect_docstring_sections(docstring):
    """
    Parse given docstring and try to detect which sections of pylatest
    document for test case are present.

    Args:
        content(string): content of an pylatest docstring

    Returns:
        tuple: list of detected sections (Section objects),
               number of test action directives
    """
    # parse docstring to get rst node tree
    nodetree = publish_doctree(source=docstring)

    # TODO: search for this kind of elements in the tree:
    # <system_message level="3" line="4" source="<string>" type="ERROR">
    # and report rst parsing errors in a useful way immediately
    # Also note that publish_doctree() reports the errors to stderr, which
    # is not that great here - TODO: reconfigure (logging involved?)
    #
    # Moreover: when some error occurs, eg. directive can't be parsed
    # properly because of some syntax problem, the resulting document tree
    # will contain those pending nodes ... but depending how serious the
    # error is, the docutils tools may not even produce any output (in which
    # case, leftover pending nodes don't concern us) ... only when the issue
    # is not serious enough, the output will be generated - and we need to
    # cope with leftover pending nodes

    # try to find any pylatest section
    detected_sections = []
    title_condition = lambda node: \
        isinstance(node, nodes.title) or isinstance(node, nodes.subtitle)
    for node in nodetree.traverse(title_condition):
        section = Section(title=node.astext())
        if section in TestCaseDoc.SECTIONS:
            detected_sections.append(section)

    # try to count all pylatest step/result directives
    test_directive_count = 0
    for node in nodetree.traverse(_teststeps_condition):
        test_directive_count += 1
    for node in nodetree.traverse(_teststeps_condition_hack):
        test_directive_count += 1

    # try to detect header pseudo section (contains name and metadata)
    meta_directive_count = 0
    nodes_title_count = 0
    for node in nodetree.traverse(pylatest.xdocutils.nodes.test_metadata_node):
        meta_directive_count += 1
    for node in nodetree.traverse(nodes.title):
        nodes_title_count += 1
    if meta_directive_count > 0 and nodes_title_count > 0:
        # here we expect that:
        # 1) header pseudosection starts with the title,
        #    which would make it the very first element in the nodetree
        # 2) this title contains name of the test case,
        #    so that title text doesn't match predefined set of sections
        title_index = nodetree.first_child_matching_class(nodes.title)
        title_value = nodetree[title_index].astext()
        if title_index == 0 and not TestCaseDoc.has_section(title=title_value):
            detected_sections.insert(1, TestCaseDoc._HEAD)

    return detected_sections, test_directive_count


# # parse docstring to get rst node tree
# nodetree = publish_doctree(source=docstring)
#
# # TODO: functions to create:
# # get_section_nodes() -> [node]
# # get_actions_nodes() -> [node]
# # extract_node(nodetree, node, str_val) -> str_val_of_node
# # But what to do with header pseudo section?
# #  - no explicit header
# #  - some pylatest nodes
