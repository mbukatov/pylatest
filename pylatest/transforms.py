# -*- coding: utf8 -*-

"""
ReStructuredText transformations for test steps and actions.

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


import sys

from docutils import nodes
from docutils import transforms


class FooBarTransform(transforms.Transform):
    """
    Collects data from pending elements and generates new rst nodes
    to replace them.
    """

    # use priority in "very late (non-standard)" range so that all
    # standard transformations will be executed before this one
    default_priority = 999

    def build_table(self, row_nodes):
        """
        Creates new table node tree for FooBar data.
        """
        table = nodes.table()
        tgroup = nodes.tgroup(cols=2)
        table += tgroup
        # TODO: headrows
        # TODO: colspec
        tbody = nodes.tbody()
        tgroup += tbody
        for row in row_nodes:
            tbody += row
        return table

    def build_row(self, foobar_id, content_nodes):
        """
        Creates new table row node tree for FooBar data.
        """
        row_node = nodes.row()
        num_node = nodes.entry()
        num_node += nodes.paragraph(text=str(foobar_id))
        row_node += num_node
        entry_node = nodes.entry()
        row_node += entry_node
        for node in content_nodes:
            entry_node += node
        return row_node

    def apply(self):
        pending_nodes = {}
        # find all pending nodes of foobar directive
        # TODO: validate id (eg. report error when conflicts are found)
        for node in self.document.traverse(nodes.pending):
            if 'foobar_id' in node.details:
                pending_nodes[node.details['foobar_id']] = node
        # generate table node tree based on data from pending elements
        row_nodes = []
        for foobar_id, pending_node in sorted(pending_nodes.iteritems()):
            row_node = self.build_row(foobar_id, pending_node.details['nodes'])
            row_nodes += row_node
        table_node = self.build_table(row_nodes)
        # replace pending element with new node struct
        # we assume that this is called on the first pending node only
        self.startnode.replace_self(table_node)
        # remove all remaining foobar pending nodes from document tree
        del pending_nodes[1]
        for pending_node in pending_nodes.itervalues():
            pending_node.parent.remove(pending_node)
