# -*- coding: utf8 -*-

"""
Python source reader module to extract pylatest data from docstrings.

TODO: Unfortunatelly current initial implementation is a terryble hack.
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


import ast
import inspect
import argparse

from docutils.core import publish_doctree
from docutils import nodes

import pylatest.client
import pylatest.nodes


def get_docstrings(ast_tree):
    """
    Returns all docstrings found in given ast tree.

    Args:
        ast_tree: parsed python code

    Returns:
        list of ``str`` objects of all docstring expressions from the ast tree
    """
    result = []
    for node in ast.walk(ast_tree):
        # docstring is a standalone string expression
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Str):
            # ignoring line number (node.lineno and node.value.lineno)
            result.append(inspect.cleandoc(node.value.s))
    return result

def sections_condition(node):
    """
    Traverse condition for filtering title nodes.
    """
    return isinstance(node, nodes.title) or isinstance(node, nodes.subtitle)

# TODO: this doesn't work because node tree still contains pending elements
# instead of test step nodes - with single exception: the very first test step
# WTF? all metadata nodes are generated just fine ...
def teststeps_condition_bypylatestnode(node):
    """
    Traverse condition for filtering nodes of test steps directives.
    """
    test_steps_directives = ("test_step_node", "test_result_node")
    for pylatest_node in test_steps_directives:
        node_class = getattr(pylatest.nodes, pylatest_node)
        if isinstance(node, node_class):
            return True
    return False

def teststeps_condition(node):
    """
    Traverse condition for filtering nodes of test steps directives.
    """
    # TODO: proper check (of at least transformation class) goes here
    if isinstance(node, nodes.pending):
        return True
    return False

# TODO: improve content detection, check possible errors, eg:
#  * test step directives should not be mixed with other content
#  * duplication of section titles
#  * tons of ther possible error states
def detect_pylatest_content(docstring):
    """
    Checks if given string contains some part of pylatest test description,
    and returns list of sections detected.

    Args:
        docstring (str): content of single docstring expression

    Returns:
        List of detected Pylatest section (eg. 'Description', 'Test Steps', ..),
        Empty list if docstring doesn't contain any pylatest data.
    """
    result = []
    # parse docstring to get rst node tree
    nodetree = publish_doctree(source=docstring)
    # try to find any pylatest section (but 'Test Steps')
    pylatest_sections = ("Description", "Setup", "Teardown")
    for node in nodetree.traverse(sections_condition):
        if node.astext() in pylatest_sections:
            result.append(node.astext())
    # TODO: resolve this hack (this is needed to find just 1st test step!)
    for node in nodetree.traverse(teststeps_condition_bypylatestnode):
        result.append("Test Steps")
        # single test step/result directive is enough
        break
    # try to find any test steps directive
    for node in nodetree.traverse(teststeps_condition):
        result.append("Test Steps")
        # single test step/result directive is enough
        break
    return result

# This fuction is just initial implementation (read: a terrible hack),
# TODO: make it more generic, it currently assumes that sections are separated
#       in dedicated docstrings
def recreate_document(pylatest_content):
    """
    Recreate pylatest test case description from docstring fragments.
    """
    pylatest_description = ""
    pylatest_setup = ""
    pylatest_teardown = ""
    pylatest_teststeps_list = []
    for sections, content_string in pylatest_content:
        section = sections[0]
        if section == "Description":
            pylatest_description = content_string
        elif section == "Setup":
            pylatest_setup = content_string
        elif section == "Teardown":
            pylatest_teardown = content_string
        elif section == "Test Steps":
            pylatest_teststeps_list.append(content_string)
    # put together test steps
    pylatest_teststeps = \
        "Test Steps\n==========\n\n" + "\n\n".join(pylatest_teststeps_list)
    # and finally, put the document back into single piece
    doc_list = []
    doc_list.append(pylatest_description)
    doc_list.append('\n\n')
    doc_list.append(pylatest_setup)
    doc_list.append('\n\n')
    doc_list.append(pylatest_teststeps)
    doc_list.append('\n\n')
    doc_list.append(pylatest_teardown)
    return "".join(doc_list)


def main():
    """
    Main function of python2pylatest cli tool.
    """
    parser = argparse.ArgumentParser(
        description='Generate rst testcase description from python source.')
    parser.add_argument(
        "filepath",
        help="path of python source code automating given testcase")
    args = parser.parse_args()

    # register pylatest rst extensions (parsing friendly plain implementation)
    pylatest.client.register_plain()

    docstrings = []
    with open(args.filepath, 'r') as python_file:
        tree = ast.parse(python_file.read())
        docstrings = get_docstrings(tree)
    # filter docstrings further, I'm interested only if docstring contains
    # part of testcase description
    pylatest_content = []
    for docstring in docstrings:
        detected_sections = detect_pylatest_content(docstring)
        if len(detected_sections) != 0:
            pylatest_content.append((detected_sections, docstring))
    rst_document = recreate_document(pylatest_content)
    # TODO: here goes error handling
    print(rst_document)
