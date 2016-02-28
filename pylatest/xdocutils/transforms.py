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

import pylatest.xdocutils.nodes


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


class PylatestTransform(transforms.Transform):
    """
    Base class of all pylatest transformations.

    Pylatest transformations (extending this base class) collect data from
    pending elements, remove them from document tree and generate rst node tree
    (which contains all data from pending elements) in the place of 1st pending
    element.
    """

    # use priority in "very late (non-standard)" range so that all
    # standard transformations will be executed before this one
    default_priority = 999

    def _find_pending_nodes(self):
        """
        Find all pending nodes (of given rst directive) in rst document tree.
        """
        raise NotImplementedError

    def _drop_pending_nodes(self):
        """
        Drop all pending nodes (of given rst directive) from rst document tree.
        """
        raise NotImplementedError

    def _create_content(self):
        """
        Generate new content which will be insterted into place where the
        1st pending element was found.
        """
        raise NotImplementedError

    def apply(self):
        self._find_pending_nodes()
        content_node = self._create_content()
        # replace current pending node with new content
        # we assume that this is called on the first pending node only
        # TODO: check the assumption
        self.startnode.replace_self(content_node)
        self._drop_pending_nodes()


class TestStepsTransform(PylatestTransform):
    """
    Base trasformation class for test steps directive.
    """

    # Action is couple of test step and result with the same action id.
    # Expected structure eg. for pending nodes of 1st step and result:
    # ``actions_dict = {1: {'test_step': node_a, 'test_result': node_b}}``
    _actions_dict = None

    def _find_pending_nodes(self):
        """
        Find all pending nodes of pylatest directive and store them in
        ``_actions_dict`` attribute.
        """
        self._actions_dict = {}
        # TODO: validate id (eg. report error when conflicts are found)
        for node in self.document.traverse(nodes.pending):
            if 'action_id' not in node.details:
                continue
            action_id = node.details['action_id']
            action_name = node.details['action_name']
            self._actions_dict.setdefault(action_id, {})[action_name] = node

    def _drop_pending_nodes(self):
        """
        Remove all pending nodes from rst document tree.
        """
        # drop current pending element from ``_actions_dict`` because this one
        # has been already removed from document tree via replace_self()
        del self._actions_dict[1]['test_step']
        # remove all remaining pylatest pending nodes from document tree
        for action_dict in self._actions_dict.values():
            for pending_node in action_dict.values():
                pending_node.parent.remove(pending_node)


class TestStepsTableTransform(TestStepsTransform):
    """
    Builds table from pending test step nodes.
    """

    def _create_content(self):
        """
        Generate table node tree based on data stored in pending elements.
        """
        row_nodes = []
        for action_id, action_nodes in sorted(self._actions_dict.items()):
            row_data = []
            # add action_id into row_data as 1st entry
            row_data.append([nodes.paragraph(text=str(action_id))])
            # for each action check if we have step and result pending node
            # this defines order of collumns in resulting table
            for col_name in ('test_step', 'test_result'):
                if col_name in action_nodes:
                    row_data.append(action_nodes[col_name].details['nodes'])
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


class TestStepsPlainTransform(TestStepsTransform):
    """
    Wrapp content from pending test step nodes in div element so that test
    steps are adressable via xpath (works with html output only).
    """

    def _create_content(self):
        p_node = nodes.paragraph()
        for action_id, action_nodes in sorted(self._actions_dict.items()):
            for col_name in ('test_step', 'test_result'):
                if col_name in action_nodes:
                    node_name = "{0:s}_node".format(col_name)
                    node = getattr(pylatest.xdocutils.nodes, node_name)()
                    # add all content nodes into step or result node
                    for c_node in action_nodes[col_name].details['nodes']:
                        node += c_node
                    node.attributes['action_id'] = action_id
                    p_node += node
        return p_node


class TestMetadataTransform(PylatestTransform):
    """
    Base trasformation class for test metadata directive.
    """

    # dictionary with metadata: meta_name -> meta_value
    _metadata_dict = None
    # list of pending nodes (so that they can be removed in the end)
    _pending_nodes = None

    def _find_pending_nodes(self):
        self._metadata_dict = {}
        self._pending_nodes = []
        # find all metadata pending nodes
        for node in self.document.traverse(nodes.pending):
            if 'meta_name' not in node.details:
                continue
            name = node.details['meta_name']
            value = node.details['meta_value']
            self._metadata_dict[name] = value
            self._pending_nodes.append(node)

    def _drop_pending_nodes(self):
        # drop current pending node from the list because it
        # has been already removed from document tree via replace_self()
        del self._pending_nodes[0]
        # remove all remaining pylatest pending nodes from document tree
        for pending_node in self._pending_nodes:
            pending_node.parent.remove(pending_node)


class TestMetadataTableTransform(TestMetadataTransform):
    """
    Builds table from pending test metadata nodes.
    """

    def _create_content(self):
        """
        Generate table node tree based on data from pending elements.
        """
        row_nodes = []
        for name, value in sorted(self._metadata_dict.items()):
            row_data = []
            row_data.append([nodes.paragraph(text=name)])
            row_data.append([nodes.paragraph(text=value)])
            row_node = build_row(row_data)
            row_nodes.append(row_node)
        table_node = build_table(row_nodes, [50, 50])
        return table_node


class TestMetadataPlainTransform(TestMetadataTransform):
    """
    Wrapp content (from metadata nodes) in span element so that metadata are
    adressable via xpath.
    """

    def _create_content(self):
        p_node = nodes.paragraph()
        for name, value in sorted(self._metadata_dict.items()):
            meta_node = pylatest.xdocutils.nodes.test_metadata_node()
            p_node += meta_node
            meta_node += nodes.paragraph(text=value)
            meta_node.attributes['name'] = name
        return p_node
