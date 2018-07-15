# -*- coding: utf8 -*-
# flake8: noqa

"""
Pylatest document tree element class module.

This module is used to generate plain html output only, it's not needed for
default html (with tables). There is a node class for each pylatest directive,
so that it's possible to wrap directive content into div or span element.

See: http://epydoc.sourceforge.net/docutils/public/docutils.nodes-module.html
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


class test_action_node(nodes.Element): pass
class requirementlist_node(nodes.Element): pass


node_class_names = [
    "test_action_node",
    "requirementlist_node",
    ]
"""A list of names of all pylatest Node subclasses."""
