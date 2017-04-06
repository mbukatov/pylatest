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


from docutils.core import publish_doctree
from docutils import nodes

from pylatest.xdocutils.nodes import test_action_node


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
        return (self.title == other.title and
                self.start_line == other.start_line and
                self.end_line == other.end_line)

    def __repr__(self):
        template = "RstSection('{}', {}, {})"
        return template.format(self.title, self.start_line, self.end_line)


class RstTestAction(object):

    def __init__(self, action_id, action_name, start_line, end_line=None):
        self.action_id = action_id
        self.action_name = action_name
        self.start_line = start_line
        self.end_line = end_line

    def __eq__(self, other):
        return (self.action_id == other.action_id and
                self.action_name == other.action_name and
                self.start_line == other.start_line and
                self.end_line == other.end_line)

    def __repr__(self):
        template = "RstTestAction({}, {}, {}, {})"
        return template.format(
            self.action_id, self.action_name, self.start_line, self.end_line)


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
    # shortcut: immediatelly return for empty doc (so that we can assume
    # nonempty nodetree later)
    if len(rst_source) == 0 or len(nodetree) == 0:
        return []
    # look for rst sections
    sections = []
    prev_section = None
    for node in [n for n in nodetree.children if isinstance(n, nodes.section)]:
        title = node.children[0].astext()
        section = RstSection(title, node.line - 1)
        sections.append(section)
        if prev_section is not None:
            prev_section.end_line = node.line - 3
        prev_section = section
    # last section ends on the last line of the rst source
    if prev_section is not None:
        prev_section.end_line = get_last_line_num(rst_source)
    # check if the node tree contains test metadata nodes
    contains_meta = False
    for node in nodetree.traverse(lambda n: isinstance(n, nodes.docinfo)):
        contains_meta = True
        break
    # look for metadata fragment and report it "as a special section"
    if contains_meta and nodetree.children[0].tagname == "title":
        if len(sections) == 0:
            # rst_source contains just the meta data fragment
            section = RstSection(None, 1, get_last_line_num(rst_source))
            sections.append(section)
        else:
            section = RstSection(None, 1, sections[0].start_line - 2)
            sections.append(section)
    # a special case: this is necessary to be able to find sections fragments
    # (rst source which contains just title and some content) - as long as rst
    # parser is concerned, it's a rst document, but wrt pylatest test case
    # document, it represent a mere fragment, particular section from a test
    # case
    if len(sections) == 0 and \
       nodetree[0].tagname == "title" and \
       rst_source[0].isalpha():
        title = nodetree[0].astext()
        section = RstSection(title, 1, get_last_line_num(rst_source))
        sections.append(section)
    return sections


def find_actions(rst_source):
    # parse rst_source string to get rst node tree
    nodetree = publish_doctree(source=rst_source)

    actions = []
    for node in nodetree.traverse(test_action_node):
        # we can't get line of the directive node directly, because docutils
        # doesn't provide it (node.line is None), but we can use the fact that
        # a paragraph node (which contains content of the directive) has line
        # attribute initialized properly
        #
        # pseudoxml tree of directive node looks like this:
        #
        # <test_action_node action_id="1" action_name="test_result">
        #     <paragraph>
        #         There are no files, output should be empty.
        #
        # where:
        #  * test_action_node.line is None
        #  * paragraph.line have a value here
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
            if next_node.tagname == "test_action_node":
                end_line = next_node.children[0].line - 4
            elif next_node.tagname == "section":
                end_line = next_node.line - 3
            else:
                end_line = next_node.line - 2
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
                #     <test_action_node action_id="1" action_name="test_step">
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
                    end_line = next_node.line - 3
                else:
                    end_line = next_node.line - 2
            else:
                # ok, it seems this node is the last one in the rst source
                end_line = get_last_line_num(rst_source)
        action_id = node.attributes['action_id']
        action_name = node.attributes['action_name']
        action = RstTestAction(action_id, action_name, start_line, end_line)
        actions.append(action)
    return actions
