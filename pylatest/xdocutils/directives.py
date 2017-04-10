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


def arguments2action_id(arguments):
    """
    Converts agruments of Rst Directive into action id.

    Note that *action* is couple of test step and result with the same
    ``action_id``.
    """
    if len(arguments) == 0:
        action_id = None
    else:
        action_id = int(arguments[0])
    return action_id


def parse_content(state, content, content_offset, options):
    """
    Parse content of a directive (via state.nexted_parse) into new anonymous
    node element.
    """
    # first of all, parse text content of this directive
    # into anonymous node element (can't be used directly in the tree)
    content_node = nodes.Element()
    state.nested_parse(content, content_offset, content_node)
    return content_node


class TestActionDirective(rst.Directive):
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
        action_id = arguments2action_id(self.arguments)

        # parse text content of this directive into anonymous node element
        # (can't be used directly in the tree)
        content_node = parse_content(
            self.state, self.content, self.content_offset, self.options)

        # create new action node
        action_node = pylatest.xdocutils.nodes.test_action_node()

        # add all content nodes into the new action node
        for content in content_node:
            action_node += content
        action_node.attributes['action_id'] = action_id
        action_node.attributes['action_name'] = self.name

        # and finally return the action node as the only result
        return [action_node]


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
