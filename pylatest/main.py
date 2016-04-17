# -*- coding: utf8 -*-

"""
Commandline script module for pylatest docutils clients.
"""

# Copyright (C) 2016 mbukatov@redhat.com
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


from pylatest.xdocutils import client


def pylatest2html():
    """
    Pylatest client which generates html output. It is similar to ``rst2html``,
    but it knows how to handle pylatest rst directives and doesn't produce
    embedded css code.
    """
    client.register_table()
    client.publish_cmdline_html()

def pylatest2htmlplain():
    client.register_plain()
    client.publish_cmdline_html()

def pylatest2man():
    # TODO: run manpage viewer immediately
    client.register_table()
    client.publish_cmdline_man()

def pylatest2pseudoxml():
    """
    This client is useful for debugging purposes only.
    """
    client.register_table()
    client.publish_cmdline_pseudoxml()
