# -*- coding: utf8 -*-

"""
ReStructuredText transformations for pylatest directives.

See: http://docutils.sourceforge.net/docs/ref/transforms.html
"""

# Copyright (C) 2015 martin.bukatovic@gmail.com
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


from docutils import nodes
from docutils import transforms

from pylatest.xdocutils.nodes import test_action_node
from pylatest.xdocutils.nodes import requirement_node
import pylatest.document


def find_test_action_nodes(document):
    """
    Find all test action nodes (of pylatest test action directive).
    """
    actions = pylatest.document.TestActions()
    # TODO: validate id (eg. report error when conflicts are found)
    for node in document.traverse(test_action_node):
        if 'action_id' not in node.attributes:  # TODO: find out why?
            continue
        action_id = node.attributes['action_id']
        action_name = node.attributes['action_name']
        actions.add(action_name, node, action_id)
    return actions


def drop_test_action_nodes(actions):
    """
    Remove all test action nodes from rst document tree.
    """
    action_node_iter = actions.iter_content()
    # skip current action node element because this one
    # has been already removed from document tree via replace_self()
    next(action_node_iter)
    # remove all remaining pylatest action nodes from document tree
    for action_node in action_node_iter:
        action_node.parent.remove(action_node)

def create_content(actions):
    """
    Generate table node tree based on data stored in test action nodes.
    """
    row_nodes = []
    for action_id, step_nodes, result_nodes in actions:
        row_data = []
        # add action_id into row_data as 1st entry
        row_data.append([nodes.paragraph(text=str(action_id))])
        # for each action check if we have step and result pending node
        # this defines order of collumns in resulting table
        for action_nodes in (step_nodes, result_nodes):
            if action_nodes is not None:
                row_data.append(action_nodes.children)
            else:
                row_data.append(nodes.paragraph())
        row_node = build_row(row_data)
        row_nodes.append(row_node)
    headrow_data = [
        nodes.paragraph(),
        [nodes.paragraph(text="Step")],
        [nodes.paragraph(text="Expected Result")],
        ]
    table_node = build_table(row_nodes, [2, 44, 44], headrow_data)
    return table_node


def build_table(row_nodes, colwidth_list, headrow_data=None):
    """
    Creates new rst table node tree.

    Args:
        row_nodes (list): list of docutils.nodes.row nodes,
            contains actual content of the rst table
        colwidth_list (list): list of width percentages for each column,
            eg.: use [10, 90] for 2 columns, 1st has 10% width, 2nd the rest

    Returns:
        docutils.nodes.table: rst table node tree which contains given rows
    """
    table = nodes.table()
    tgroup = nodes.tgroup(cols=len(colwidth_list))
    table += tgroup
    for colwidth in colwidth_list:
        colspec = nodes.colspec(colwidth=colwidth)
        tgroup += colspec
    if headrow_data is not None:
        thead = nodes.thead()
        tgroup += thead
        head_row_node = build_row(headrow_data)
        thead += head_row_node
    tbody = nodes.tbody()
    tgroup += tbody
    for row in row_nodes:
        tbody += row
    return table


def build_row(row_data):
    """
    Creates new rst table row node tree.

    Args:
        row_data (list): list of rst nodes with content of the row,
            length of the list should match number of columns in the table

    Returns:
        docutils.nodes.row: rst row node tree which contains given data
    """
    row_node = nodes.row()
    # create entry nodes for data
    for content_nodes in row_data:
        entry_node = nodes.entry()
        row_node += entry_node
        for node in content_nodes:
            entry_node += node
    return row_node


class TestActionsTableTransform(transforms.Transform):
    """
    Builds doctree table from pylatest test action nodes.

    Pylatest transformations (extending this base class) collect data from
    test action nodes, remove them from document tree and generate rst node
    tree (which contains all data from test action nodes) in the place of 1st
    such node.
    """

    # use priority in "very late (non-standard)" range so that all
    # standard transformations will be executed before this one
    default_priority = 999

    def apply(self):
        actions = find_test_action_nodes(self.document)
        if len(actions) == 0:
            return
        content_node = create_content(actions)
        startnode = next(actions.iter_content())
        # replace current pending node with new content
        # we assume that this is called on the first pending node only
        # TODO: check the assumption
        startnode.replace_self(content_node)
        drop_test_action_nodes(actions)


class TestActionsPlainIdTransform(transforms.Transform):
    """
    Add/update action IDs into test action nodes (if needed).
    """

    # use priority in "very late (non-standard)" range so that all
    # standard transformations will be executed before this one
    default_priority = 999

    def apply(self):
        actions = pylatest.document.TestActions()
        for node in self.document.traverse(test_action_node):
            action_id = node.attributes.get('action_id')
            action_name = node.attributes['action_name']
            new_action_id = actions.add(action_name, node, action_id)
            # update action id of the node
            node.attributes['action_id'] = new_action_id


class RequirementSectionTransform(transforms.Transform):
    """
    Builds doctree section from pylatest requirement node.
    """

    # use priority in "very late (non-standard)" range so that all
    # standard transformations will be executed before this one
    default_priority = 999

    def apply(self):
        for node in self.document.traverse(requirement_node):
            section_node = nodes.section()
            # header of the section
            title = "Requirement {0}".format(node.attributes['req_id'])
            section_node += nodes.title(text=title)
            # see docutils.nodes.Element docstring for description of both
            # 'ids' and 'names' attributes (necessary for table of contents)
            # attr ids: list of unique keys
            section_node.attributes['ids'] = [nodes.make_id(title)]
            # attr names: list of element names generated from title or content
            section_node.attributes['names'] = [
                nodes.fully_normalize_name(title)]
            # priority paragraph (if priority is specified)
            if 'priority' in node.attributes:
                text = "Priority: {0}".format(node.attributes['priority'])
                prio_node = nodes.paragraph(text=text)
                section_node += prio_node
            # and a paragraph with all content of the directive
            for content_node in node:
                section_node += content_node
            # and finally: replace requirement node with just build section
            node.replace_self(section_node)
