# -*- coding: utf8 -*-

"""
Commandline script module for pylatest docutils clients.

See: https://docutils.readthedocs.io/en/sphinx-docs/api/cmdline-tool.html
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


import os

from pylatest.xdocutils.core import pylatest_publish_cmdline


def pylatest2html():
    """
    Pylatest client which generates html output. It is similar to ``rst2html``,
    but it knows how to handle pylatest rst directives and doesn't produce
    embedded css code.
    """
    pylatest_publish_cmdline(writer_name='html')


def pylatest2htmlplain():
    pylatest_publish_cmdline(writer_name='html', use_plain=True)


def pylatest2pseudoxml():
    """
    This client is useful for debugging purposes only.
    """
    pylatest_publish_cmdline(writer_name='pseudoxml', use_plain=True)


def pylatest_preview():
    """
    Preview front-end tool based on manpage output.

    Constructs a pipe which would look like this::

        pylatest-rst2man testcase.rst | man -l -
    """
    r_fd, w_fd = os.pipe()
    pid = os.fork()
    if pid == 0:
        # child process
        os.close(r_fd)
        os.dup2(w_fd, 1)
        pylatest_publish_cmdline(writer_name='manpage')
        os._exit(0)
    else:
        # parent process
        os.close(w_fd)
        os.dup2(r_fd, 0)
        os.execv('/usr/bin/man', ["man", "-l", "-"])
