# -*- coding: utf8 -*-

"""
ReStructuredText directives for test steps and actions.
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
import os.path

from docutils import nodes
from docutils.parsers import rst


class Hello(rst.Directive):
    """
    Hello World rst directive (this is just minimal example).
    """

    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    has_content = False

    def run(self):
        content = "Hello World {0}!".format(self.arguments[0])
        node = nodes.paragraph(text=content)
        node_list = [node]
        return node_list


class SimpleAction(rst.Directive):
    """
    Simple action directive.
    """

    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    has_content = True

    def run(self):
        self.assert_has_content()
        # TODO: proper error handling
        action_id = int(self.arguments[0])
        # setup header node
        head_text = "There is action #{0}.".format(action_id)
        head_node = nodes.paragraph(text=head_text)
        # setup list node
        list_node = nodes.enumerated_list()
        # add items with content into list node
        for line in self.content:
            # TODO: find a better node for text content
            # text_node = nodes.Text(line) ?
            text_node = nodes.inline(text=line)
            item_node = nodes.list_item()
            item_node += text_node
            list_node += item_node
        # construct final result
        node_list = [head_node, list_node]
        return node_list
