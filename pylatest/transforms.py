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

    def apply(self):
        pending = self.startnode

        # TODO: check: self.document.traverse()
        # TODO: try to generate table

        # create node struct to wrap data from pending node
        # yeah, this way is kind of silly, but we need to start somewhere
        list_node = nodes.enumerated_list()
        item_node = nodes.list_item()
        for node in pending.details['nodes']:
            item_node += node
        list_node += item_node

        # replace pending element with new node
        self.startnode.replace_self(list_node)
