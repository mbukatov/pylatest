# -*- coding: utf8 -*-

"""
Pylatest extension of HTMLTranslator

This module contains functions which extends
docutils.writers.html4css1.HTMLTranslator class with implementation of custom
pylatest nodes (see pylatest.xdocutils.nodes module).
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


def visit_test_step_node(self, node):
    attributes = {
        'class': 'pylatest_action',
        'action_name': 'step',
        'action_id': node.attributes['action_id'],}
    self.body.append(self.starttag(node, 'div', **attributes))

def depart_test_step_node(self, node):
    self.body.append('\n</div>\n')

def visit_test_result_node(self, node):
    attributes = {
        'class': 'pylatest_action',
        'action_name': 'result',
        'action_id': node.attributes['action_id'],}
    self.body.append(self.starttag(node, 'div', **attributes))

def depart_test_result_node(self, node):
    self.body.append('\n</div>\n')

def visit_test_metadata_node(self, node):
    attributes = {
        'class': 'pylatest_metadata',
        'name': node.attributes['name'],}
    self.body.append(self.starttag(node, 'span', **attributes))

def depart_test_metadata_node(self, node):
    self.body.append('</span>\n')

def visit_requirement_node(self, node):
    attributes = {
        'class': 'pylatest_requirement',
        'id': node.attributes['id'],}
    self.body.append(self.starttag(node, 'div', **attributes))

def depart_requirement_node(self, node):
    self.body.append('\n</div>\n')
