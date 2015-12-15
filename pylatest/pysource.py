# -*- coding: utf8 -*-

"""
Python source reader module to extract pylatest data from docstrings.
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
import ast
import inspect
import sys

from docutils.core import publish_doctree
from docutils import nodes

import pylatest.client
import pylatest.nodes


"""
List of headers of mandatory sections in pylatest rst document (order matters).
"""
PYLATEST_SECTIONS = ("Description", "Setup", "Test Steps", "Teardown")


def get_docstrings(ast_tree):
    """
    Returns all docstrings (anonymous string literals) found in given python
    ast node tree.

    Args:
        ast_tree: python ast node tree

    Returns:
        list of (``str``, ``int``) objects of all docstring expressions from
        the ast tree (string content and it's line number)
    """
    result = []
    for node in ast.walk(ast_tree):
        # docstring is a standalone string expression
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Str):
            result.append((inspect.cleandoc(node.value.s), node.lineno))
    return result


class PylatestDocument(object):
    """
    Pylatest rst document (test case description).
    """

    def __init__(self):
        self._docstrings = [] # list of docstrings with at least one section
        self._test_steps = [] # dosctrings with just test step directives
        self._section_dict = {} # section name -> list of docstrings
        self._err_dict = {} # lineno -> list of err msg
        self._run_errs = [] # runtile error list (after reading docstrings)

    # TODO: this doesn't work because node tree still contains pending elements
    # instead of test step nodes - with single exception: the very first test
    # step - WTF? all metadata nodes are generated just fine ...
    @staticmethod
    def _teststeps_condition(node):
        """
        Traverse condition for filtering nodes of test steps directives.
        """
        test_steps_directives = ("test_step_node", "test_result_node")
        for pylatest_node in test_steps_directives:
            node_class = getattr(pylatest.nodes, pylatest_node)
            if isinstance(node, node_class):
                return True
        return False

    @staticmethod
    def _teststeps_condition_hack(node):
        """
        Traverse condition for filtering nodes of test steps directives.

        This is a quick hack to overcome issue with ``_teststeps_condition()``.
        """
        # TODO: proper check (of at least transformation class) goes here
        if isinstance(node, nodes.pending):
            return True
        return False

    def _add_error(self, msg, lineno=None):
        """
        Add error into error list.
        """
        if lineno is None:
            self._run_errs.append(msg)
        else:
            self._err_dict.setdefault(lineno, []).append(msg)

    def has_errors(self):
        """
        Return true if errors were logged during parsing and generation.
        """
        return len(self._err_dict) > 0 or len(self._run_errs) > 0

    def errors(self):
        """
        Return error iterator (sorted by line number).
        """
        for lineno, err_list in sorted(self._err_dict.items()):
            for err in err_list:
                yield lineno, err

    def errors_lastrecreate(self):
        """
        Return iterator for error found during last ``recreate()`` run.
        """
        return iter(self._run_errs)

    def add_docstring(self, docstring, lineno):
        """
        Look for some part of pylatest test description data in given string,
        and add it into this pylatest document if such data are found.

        Args:
            docstring (str): content of single docstring expression

        Returns:
            True if given docstring contains pylatest data and were added,
            Fase otherwise.
        """
        # parse docstring to get rst node tree
        nodetree = publish_doctree(source=docstring)

        # try to find any pylatest section
        detected_sections = []
        condition = lambda node: \
            isinstance(node, nodes.title) or isinstance(node, nodes.subtitle)
        for node in nodetree.traverse(condition):
            if node.astext() in PYLATEST_SECTIONS:
                detected_sections.append(node.astext())

        # try to count all pylatest step/result directives
        test_directive_count = 0
        for node in nodetree.traverse(self._teststeps_condition):
            test_directive_count += 1
        for node in nodetree.traverse(self._teststeps_condition_hack):
            test_directive_count += 1

        if len(detected_sections) == 0 and test_directive_count == 0:
            return False
        if len(detected_sections) == 0 and test_directive_count > 0:
            self._test_steps.append(docstring)
            return True
        if len(detected_sections) > 0 and test_directive_count == 0:
            if "Test Steps" in detected_sections:
                # we have Test Steps section without test step directives
                msg = "found 'Test Steps' section without test step direcives"
                self._add_error(msg, lineno)
            self._docstrings.append(docstring)
            for section in detected_sections:
                self._section_dict.setdefault(section, []).append(docstring)
            return True
        if len(detected_sections) > 0 and test_directive_count > 0:
            if "Test Steps" not in detected_sections:
                msg = ("docstring with multiple sections contains test step"
                      " directives, but no 'Test Steps' section was found")
                self._add_error(msg, lineno)
            self._docstrings.append(docstring)
            for section in detected_sections:
                self._section_dict.setdefault(section, []).append(docstring)
            return True

    @property
    def sections(self):
        """
        Get list of sections this document contains so far.
        """
        return self._section_dict.keys()

    def recreate(self):
        """
        Recreate pylatest test case description from docstring fragments.
        """
        # reset err list
        self._run_errs = []

        # nothing has been found
        if len(self._docstrings) == 0:
            return ""

        # report missing sections
        for section in PYLATEST_SECTIONS:
            if section not in self._section_dict:
                if section == "Test Steps" and len(self._docstrings) > 1:
                    # test steps may be in standalone directives
                    continue
                msg = "{0:s} section is missing.".format(section)
                self._add_error(msg)

        # when everything is just in a single string
        if len(self._docstrings) == 1:
            content_string = self._docstrings[0]
            return content_string + '\n'

        # document is splitted across multiple docstrings
        rst_list = []
        docstrings_used = set()
        for section in PYLATEST_SECTIONS:
            docstrings = self._section_dict.get(section)
            if docstrings is None and section == "Test Steps":
                # put together test steps
                if len(self._test_steps) > 0:
                    rst_list.append("Test Steps\n==========")
                    teststeps = "\n\n".join(self._test_steps)
                    rst_list.append(teststeps)
                else:
                    msg = "test steps/actions directives are missing"
                    self._add_error(msg)
            if docstrings is None:
                continue
            if len(docstrings) > 1:
                msg = "multiple docstrings with {0:s} section found"
                self._add_error(msg.format(section))
            # case with multiple docstrings for one section is invalid,
            # but add them all anyway to make debugging easier
            for docstring in docstrings:
                if docstring not in docstrings_used:
                    rst_list.append(docstring)
                    docstrings_used.add(docstring)

        return "\n\n".join(rst_list) + '\n'


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

    # get all python docstrings
    docstrings = []
    with open(args.filepath, 'r') as python_file:
        tree = ast.parse(python_file.read())
        docstrings = get_docstrings(tree)

    # filter docstrings, I'm interested only if docstring contains
    # part of pylatest testcase description
    doc = PylatestDocument()
    for docstring, lineno in docstrings:
        status = doc.add_docstring(docstring, lineno)
        # TODO: do some debug output (status == True for valid pylatest data)

    # report all errors found so far
    for lineno, error in doc.errors():
        msg = "Error on line {0:d}: {1:s}"
        print(msg.format(lineno, error), file=sys.stderr)

    # TODO: try except
    rst_document = doc.recreate()

    # report all runtime errors
    for error in doc.errors_lastrecreate():
        print("Error: {0:s}".format(error), file=sys.stderr)

    print(rst_document, end='')

    if doc.has_errors():
        return 1
