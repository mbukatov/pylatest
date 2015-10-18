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

from docutils.parsers import rst
import docutils.nodes


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
        node = docutils.nodes.paragraph(text=content)
        node_list = [node]
        return node_list
