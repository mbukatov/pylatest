#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
Docutils client dev Hello World example.
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


from docutils.parsers.rst import directives
from docutils.core import publish_cmdline

from pylatest.directives import Hello
from pylatest.directives import SimpleAction


# register custom pylatest rst directives
# see: http://docutils.sourceforge.net/docs/howto/rst-directives.html
directives.register_directive("hello", Hello)
directives.register_directive("action", SimpleAction)

# override default settings
# see: http://docutils.sourceforge.net/docs/api/publisher.html
# see: http://docutils.sourceforge.net/docs/user/config.html
overrides = {
    # don't embed default stylesheed
    'embed_stylesheet': False,
    # don't use stylesheet at all
    'stylesheet_path': None,
    }

# see: http://docutils.sourceforge.net/docs/api/cmdline-tool.html
publish_cmdline(writer_name='html', settings_overrides=overrides)
