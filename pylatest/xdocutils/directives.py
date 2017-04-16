# -*- coding: utf8 -*-

"""
ReStructuredText directives for test steps (actions).

Note that binding between name of directive (as used in rst file) and rst
directive class which implements it is defined in pylatest.xdocutils.client
module.
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
from docutils.parsers import rst

import pylatest.xdocutils.nodes


class OldTestActionDirective(rst.Directive):
    """
    Implementation of ``test_step`` and ``test_result`` directives for
    either human readable table representation for html output or further
    processing (aka plain output), eg. checking particular part of resulting
    document.
    """

    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    has_content = True

    def run(self):
        # each pylatest directive in the rst document has mandatory action id
        # (starts from 1), so there is either just one or no pylatest directive
        # with action_id == 1
        # note:
        # action is couple of test step and result with the same action_id
        action_id = int(self.arguments[0])

        # parse text content of this directive into anonymous node element
        # (can't be used directly in the tree)
        content_node = nodes.Element()
        self.state.nested_parse(
            self.content, self.content_offset, content_node)

        # create new action node
        action_node = pylatest.xdocutils.nodes.test_action_node()

        # add all content nodes into the new action node
        for content in content_node:
            action_node += content
        action_node.attributes['action_id'] = action_id
        action_node.attributes['action_name'] = self.name

        # and finally return the action node as the only result
        return [action_node]


class TestActionDirective(rst.Directive):
    """
    Implementation of ``test_action`` directive for either human readable table
    representation for html output or further processing (aka plain output),
    eg. checking particular part of resulting document.
    """

    required_arguments = 0
    optional_arguments = 0
    has_content = True

    def run(self):
        node_list = []

        # parse text content of this directive into anonymous node element
        # (which can't be used directly in the tree)
        content_node = nodes.Element()
        self.state.nested_parse(
            self.content, self.content_offset, content_node)

        # field list node tree looks like this:
        #
        #   <field_list>
        #       <field>
        #           <field_name>
        #               result
        #           <field_body>
        #               <paragraph>
        #                   Output should be empty.

        # TODO: report error when step is missing
        # TODO: report error for unknown field_name (neither step nor result)

        # search for field nodes in parsed content
        for field in content_node.traverse(nodes.field):
            # TODO: better error checking
            # TODO: find out details of valid states of nodetree of field list
            # make clear my intentions here (in case something breaks later)
            assert field[0].tagname == "field_name"
            assert field[1].tagname == "field_body"
            field_name_value = field[0][0]  # text node
            field_body_node = field[1]
            # create action node
            action_node = pylatest.xdocutils.nodes.test_action_node()
            action_name = "test_{}".format(field_name_value)
            action_node.attributes['action_name'] = action_name
            action_node.attributes['action_id'] = None
            for child_node in field_body_node:
                action_node += child_node
            node_list.append(action_node)

        return node_list


class RequirementDirective(rst.Directive):
    """
    Implementation of ``requirement`` rst directive.
    """

    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    has_content = True
    option_spec = {
        'priority': str,
        }

    def run(self):
        self.assert_has_content()
        req_id = self.arguments[0]
        node = pylatest.xdocutils.nodes.requirement_node()
        node.attributes['req_id'] = req_id
        if 'priority' in self.options:
            node.attributes['priority'] = self.options['priority']
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]
