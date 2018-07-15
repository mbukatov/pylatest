# -*- coding: utf8 -*-

"""
Generator of pylatest test initial skeleton files for new test cases based
on predefined testcase template.

Example of usage, following command::

    $ pylatest-template --author john@example.com foobarcase
    $ ls
    foobarcase.rst
    $ grep '^:author:' foobarcase.rst
    :author: john@example.com

where ``pylatest-template`` is command line tool which uses ``main()``
function from this module.
"""

# Copyright (C) 2015 mbukatov@redhat.com
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


import argparse
import getpass
import os
import platform
import string

import pylatest


def create_file(template_name, new_name, variables):
    """
    Creates new file based on given template.

    Args:
        template_name (str): basename of the template (eg. ``template.rst``)
        new_name (str): basename of new file (eg. ``foobar.rst``)
        variables: dict with template variables to expand
    """
    src_path = os.path.join(
        pylatest.__path__[0], "templates", template_name + '.rst')
    new_path = os.path.join(os.getcwd(), new_name + '.rst')
    with open(src_path, 'r') as src_file, open(new_path, 'w') as new_file:
        content = string.Template(src_file.read())
        new_file.write(content.substitute(**variables))

def generate_default_author():
    """
    Generates default author (used when no author is specified).
    """
    username = getpass.getuser()
    hostname = platform.node()
    return "{0:s}@{1:s}".format(username, hostname)

def main():
    """
    Main function of pylatest-template cli tool.
    """
    parser = argparse.ArgumentParser(
        description=(
            'Generate rst file for new testcase '
            'based on predefined template.'))
    parser.add_argument(
        '-a',
        '--author',
        default=generate_default_author(),
        help="author of the testcase (eg. foo@example.com)")
    parser.add_argument(
        '-t',
        '--type',
        default="testcase",
        help="type of pylatest template (eg. testcase)")
    parser.add_argument(
        "basename",
        help="basename for new testcase without suffix")
    args = parser.parse_args()

    # TODO: try to read config (eg. author and others in the future) from
    # config file in ~/.config/pylatest.conf as well

    # TODO: do not overwrite files if already exists by default, add force flag

    # TODO proper error checking

    # TODO: make possible to pass more metadata than just author
    variables = {
        "tc_metadata_author": args.author,
        }
    create_file(args.type, args.basename, variables)
