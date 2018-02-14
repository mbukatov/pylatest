# -*- coding: utf8 -*-

"""
Pylatest Quickstart module.

Quickly setup documentation source to work with Sphinx/Pylatest project.
The code extending sphinx.quickstart module is based on hierogliph.quickstart
module by Nathan Yergler (see full copyright notice below).

Note that this is a little hack (although very useful in our case), Sphinx
itself is not designed with extending quickstart tool in mind.
"""

# Copyright (C) 2017 Martin Bukatovič <martin.bukatovic@gmail.com>
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
#
# This file incorporates work covered by the following copyright and
# permission notice:
#
#     Copyright (c) 2012-2014, Nathan Yergler
#     All rights reserved.
#
#     Redistribution and use in source and binary forms, with or without
#     modification, are permitted provided that the following conditions are
#     met:
#
#     Redistributions of source code must retain the above copyright notice,
#     this list of conditions and the following disclaimer.
#
#     Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#
#     Neither the name of the creator nor the names of its contributors may
#     be used to endorse or promote products derived from this software
#     without specific prior written permission.
#
#     THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#     "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#     LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#     A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#     HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#     SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#     LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#     DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#     THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#     (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#     OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


from __future__ import print_function
import textwrap

from sphinx.util.console import bold, nocolor, color_terminal
import sphinx.quickstart


# TODO: extend Makefile_t with new output types (later, when needed)
# TODO: extend conf.py_t with new options (later, when needed)
# note: this can't be done directly with latest sphinx (see
# https://github.com/nyergler/hieroglyph/issues/120), I would need edit the
# result


def ask_user(d):
    """
    Wrap sphinx.quickstart.ask_user and add additional questions.
    """

    # print welcome message
    print(bold('Welcome to the Pylatest quickstart utility.'))
    msg = textwrap.dedent('''
    This will ask questions for creating a Pylatest project, and then ask
    some basic Sphinx questions.
    ''')
    print(msg)

    # set a few defaults for Pylatest use case
    d.update({
        # 'ext_autodoc': ,
        # 'ext_doctest': ,
        'ext_intersphinx': True,
        # 'ext_todo': True,
        # 'ext_coverage': ,
        # 'ext_imgmath': ,
        # 'ext_mathjax': ,
        # 'ext_ifconfig': ,
        'ext_viewcode': True,
        # 'ext_githubpages': ,
        'makefile': True,
        'batchfile': False,
        'extensions': ['pylatest'],
        })

    # ask some questions (sphinx-quickstart will not ask this again)
    if 'project' not in d:
        print(('The project name will occur in several places '
               'in the built documentation.'))
        sphinx.quickstart.do_prompt(d, 'project', 'Project name')
    if 'author' not in d:
        sphinx.quickstart.do_prompt(d, 'author', 'Author(s) or Team name')

    # TODO: ask about pylatest otions here (later, when needed)

    # ask original Sphinx questions
    print()
    sphinx.quickstart.ask_user(d)


def main():
    """
    Main function of pylatest-quickstart command line tool.
    """
    if not color_terminal():
        nocolor()
    d = {}
    try:
        ask_user(d)
    except (KeyboardInterrupt, EOFError):
        print()
        print('[Interrupted.]')
        return 130  # 128 + SIGINT
    sphinx.quickstart.generate(d)
