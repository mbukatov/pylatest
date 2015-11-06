#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""
Pylatest client which generates html output.

Using this custom docutils client is necessary because we need to register
custom pylatest rst directives. Eg. if you use plain rst2html from docutils
to process pylatest rst files, it would report warnings about unknown
rst directives.
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

from pylatest.directives import PylatestDirective


# register custom pylatest rst directives
# see: http://docutils.sourceforge.net/docs/howto/rst-directives.html
directives.register_directive("test_step", PylatestDirective)
directives.register_directive("test_result", PylatestDirective)

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
