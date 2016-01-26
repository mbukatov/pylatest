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


from __future__ import print_function
import argparse
import ast
import inspect
import sys

from docutils.core import publish_doctree
from docutils import nodes

from pylatest.document import SECTIONS
import pylatest.client
import pylatest.nodes


def get_string_literals(content):
    """
    Returns all anonymous string literals found in given content of python
    source file.

    Args:
        content(string): content of a python source file

    Returns:
        list of (``str``, ``int``) objects of all docstring expressions from
        the ast tree (string content and it's line number)
    """
    result = []
    ast_tree = ast.parse(content)
    for node in ast.walk(ast_tree):
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Str):
            result.append((inspect.cleandoc(node.value.s), node.lineno))
    return result

def classify_docstring(docstring):
    """
    Classify given docstring, if pylatest content is detected, extract
    list of pylatest test case ids and docstring rst content.

    Args:
        content(string): content of an anonymous python string literal

    Returns:
        tuple: (is_pylatest_docstring(bool), doc_id_list(list), content(string))
    """
    pylatest_mark = "@pylatest"
    if docstring.startswith(pylatest_mark):
        pylatest_header, _, docstring = docstring.partition('\n')
        doc_id_list = []
        id_str = pylatest_header[len(pylatest_mark):].lstrip()
        if len(id_str) > 0:
            doc_id_list = id_str.split(' ')
        return (True, doc_id_list, docstring)
    else:
        return (False, [], docstring)

def extract_documents(source):
    """
    Try to extract pylatest docstrings from given string (content of
    a python source file) and generate PylatestDocument(s) from it.

    Returns:
        list of PylatestDocument items generated from given python source
    """
    # doc_id (aka testcase id) -> pylatest document object (aka test case doc)
    doc_dict = {}
    for docstring, lineno in get_string_literals(source):
        is_pylatest_str, doc_id_list, content = classify_docstring(docstring)
        if is_pylatest_str:
            if len(doc_id_list) == 0:
                # when no id is detected, create special document without id
                doc_id_list = [None]
            for doc_id in doc_id_list:
                doc = doc_dict.setdefault(doc_id, PylatestDocument())
                status = doc.add_docstring(content, lineno)
                # TODO: do some debug output
                # (status == True for valid pylatest data)
    return doc_dict


class PylatestDocument(object):
    """
    Pylatest rst document (test case description) extracted from python
    source code (implementing the test case).
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
            if node.astext() in SECTIONS:
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
        for section in SECTIONS:
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
        for section in SECTIONS:
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
    Main function of py2pylatest cli tool.
    """
    parser = argparse.ArgumentParser(
        description='Generate rst testcase description from python source.')
    parser.add_argument(
        "filepath",
        help="path of python source code automating given testcase")
    args = parser.parse_args()

    # register pylatest rst extensions (parsing friendly plain implementation)
    pylatest.client.register_plain()

    with open(args.filepath, 'r') as python_file:
        source_content = python_file.read()
        doc_dict = extract_documents(source_content)

    retcode = 0

    for doc_id, doc in doc_dict.items():
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
        if len(doc_dict) > 1:
            print()
        if doc.has_errors():
            retcode = 1

    return retcode
