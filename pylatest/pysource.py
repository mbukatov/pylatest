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
import os
import sys

from docutils.core import publish_doctree
from docutils import nodes

from pylatest.document import TestCaseDoc
import pylatest.xdocutils.client
import pylatest.xdocutils.nodes


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
        a tuple with:
            is_pylatest_docstring(bool)
            doc_id_list(list)
            content(string)
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

    Args:
        source(string): content of a python source file

    Returns:
        list of PylatestDocument items generated from given python source
    """
    # doc_id (aka testcase id) -> pylatest document object (aka test case doc)
    doc_dict = {}
    default_doc = PylatestDocument()
    for docstring, lineno in get_string_literals(source):
        is_pylatest_str, doc_id_list, content = classify_docstring(docstring)
        if is_pylatest_str:
            if len(doc_id_list) == 0:
                # when no id is detected, create special document without id
                doc_id_list = [None]
            elif "default" in doc_id_list:
                status = default_doc.add_docstring(content, lineno)
                continue
            for doc_id in doc_id_list:
                doc = doc_dict.setdefault(doc_id, PylatestDocument())
                status = doc.add_docstring(content, lineno)
                # TODO: do some debug output
                # (status is True for a valid pylatest data)
                assert status is True
    # allow all document objects to find defaults if needed
    if not default_doc.is_empty:
        for doc in doc_dict.values():
            doc.default_doc = default_doc
    return doc_dict

# TODO: this doesn't work because node tree still contains pending elements
# instead of test step nodes - with single exception: the very first test
# step - WTF? all metadata nodes are generated just fine ...
def _teststeps_condition(node):
    """
    Traverse condition for filtering nodes of test steps directives.
    """
    test_steps_directives = ("test_step_node", "test_result_node")
    for pylatest_node in test_steps_directives:
        node_class = getattr(pylatest.xdocutils.nodes, pylatest_node)
        if isinstance(node, node_class):
            return True
    return False

def _teststeps_condition_hack(node):
    """
    Traverse condition for filtering nodes of test steps directives.

    This is a quick hack to overcome issue with ``_teststeps_condition()``.
    """
    # TODO: proper check (of at least transformation class) goes here
    if isinstance(node, nodes.pending):
        return True
    return False

def detect_docstring_sections(docstring):
    """
    Parse given docstring and try to detect which sections of pylatest
    document for test case are present.

    Args:
        content(string): content of an pylatest docstring

    Returns:
        tuple: (list of detected sections, number of test action directives)
    """
    # parse docstring to get rst node tree
    nodetree = publish_doctree(source=docstring)

    # TODO: search for this kind of elements in the tree:
    # <system_message level="3" line="4" source="<string>" type="ERROR">
    # and report rst parsing errors in a useful way immediately
    # Also note that publish_doctree() reports the errors to stderr, which
    # is not that great here - TODO: reconfigure (logging involved?)

    # try to find any pylatest section
    detected_sections = []
    title_condition = lambda node: \
        isinstance(node, nodes.title) or isinstance(node, nodes.subtitle)
    for node in nodetree.traverse(title_condition):
        if TestCaseDoc.has_section(node.astext()):
            detected_sections.append(node.astext())

    # try to count all pylatest step/result directives
    test_directive_count = 0
    for node in nodetree.traverse(_teststeps_condition):
        test_directive_count += 1
    for node in nodetree.traverse(_teststeps_condition_hack):
        test_directive_count += 1

    # try to detect header pseudo section (contains name and metadata)
    meta_directive_count = 0
    nodes_title_count = 0
    for node in nodetree.traverse(pylatest.xdocutils.nodes.test_metadata_node):
        meta_directive_count += 1
    for node in nodetree.traverse(nodes.title):
        nodes_title_count += 1
    if meta_directive_count > 0 and nodes_title_count > 0:
        # here we expect that:
        # 1) header pseudosection starts with the title,
        #    which would make it the very first element in the nodetree
        # 2) this title contains name of the test case,
        #    so that title text doesn't match predefined set of sections
        title_index = nodetree.first_child_matching_class(nodes.title)
        if title_index == 0 and \
                not TestCaseDoc.has_section(nodetree[title_index].astext()):
            detected_sections.insert(1, TestCaseDoc._HEAD.title)

    return detected_sections, test_directive_count


class PylatestDocument(object):
    """
    Pylatest rst document (test case description) extracted from python
    source code (implementing the test case).
    """

    def __init__(self):
        # content
        self._docstrings = []
        """
        list of docstrings with at least one section
        """
        self._section_dict = {}
        """
        section name -> list of docstrings
        """
        self._test_actions = []
        """
        dosctrings with test step/result directives only
        """
        self.default_doc = None
        """
        document object with default content
        """
        # errors
        self._err_dict = {}
        """
        lineno -> list of err msg
        """
        self._run_errs = []
        """
        runtile error list (after reading docstrings)
        """
        # state
        self.is_empty = True

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

    def _add_section(self, docstring, lineno, sections):
        """
        Add docstring which contains given sections.
        """
        self._docstrings.append(docstring)
        for section in sections:
            self._section_dict.setdefault(section, []).append(docstring)

    def _add_test_actions(self, docstring, lineno):
        """
        Add docstring which contains some test step or result directives.
        """
        self._test_actions.append(docstring)

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
        sections, test_directive_count = detect_docstring_sections(docstring)

        if len(sections) == 0 and test_directive_count == 0:
            status_success = False
        elif len(sections) == 0 and test_directive_count > 0:
            self._add_test_actions(docstring, lineno)
            status_success = True
        elif len(sections) > 0 and test_directive_count == 0:
            if "Test Steps" in sections:
                # we have Test Steps section without test step directives
                msg = "found 'Test Steps' section without test step direcives"
                self._add_error(msg, lineno)
            self._add_section(docstring, lineno, sections)
            status_success = True
        elif len(sections) > 0 and test_directive_count > 0:
            if "Test Steps" not in sections:
                msg = ("docstring with multiple sections contains test step"
                      " directives, but no 'Test Steps' section was found")
                self._add_error(msg, lineno)
            self._add_section(docstring, lineno, sections)
            status_success = True

        if status_success:
            self.is_empty = False
        return status_success

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

        # import default sections
        if self.default_doc is not None:
            for section in ("Description", "Setup", "Teardown"):
                if section not in self.sections \
                    and section in self.default_doc.sections:
                    # TODO: log this event (info or debug)
                    # TODO: improve error checks (we assume few things here)
                    def_section = self.default_doc._section_dict[section][0]
                    self.add_docstring(def_section, 1)

        # report missing sections
        for section in TestCaseDoc.SECTIONS_ALL:
            if section.title not in self._section_dict:
                if section == TestCaseDoc.STEPS and len(self._docstrings) > 1:
                    # test steps may be in standalone directives
                    continue
                msg = "{0} section is missing.".format(section)
                self._add_error(msg)

        # when everything is just in a single string
        if len(self._docstrings) == 1:
            content_string = self._docstrings[0]
            return content_string + '\n'

        # document is splitted across multiple docstrings
        rst_list = []
        docstrings_used = set()
        for section in TestCaseDoc.SECTIONS_ALL:
            docstrings = self._section_dict.get(section.title)
            if docstrings is None and section == TestCaseDoc.STEPS:
                # put together test steps
                if len(self._test_actions) > 0:
                    rst_list.append(section.get_rst_header())
                    teststeps = "\n\n".join(self._test_actions)
                    rst_list.append(teststeps)
                else:
                    msg = "test steps/actions directives are missing"
                    self._add_error(msg)
            if docstrings is None:
                continue
            if len(docstrings) > 1:
                msg = "multiple docstrings with {0} section found"
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
        "-c", "--create-files", action="store_true", default=False,
        help="write pylatest rst documenent(s) into file(s) instead of stdout")
    parser.add_argument(
        "-d", "--basedir", action="store",
        help=(
            "path to directory where rst files should be generated "
            "(use with --create-files)"))
    parser.add_argument(
        "--default-filename", action="store",
        help=(
            "default filename for docstring without id "
            "(use with --create-files)"))
    parser.add_argument(
        "--enforce-id", action="store_true", default=False,
        help="fail outright when no docstring id is found")
    parser.add_argument(
        "-l", "--list", action="store_true", default=False,
        help="just list testcases in given python file without exporting")
    parser.add_argument(
        "filepath",
        help="path of python source code automating given testcase")
    args = parser.parse_args()

    if args.default_filename and args.enforce_id:
        msg = (
            "Error: using both --default-filename "
            "and --enforce-id doesn't make sense")
        print(msg, file=sys.stderr)
        return 1

    # register pylatest rst extensions (parsing friendly plain implementation)
    pylatest.xdocutils.client.register_plain()

    with open(args.filepath, 'r') as python_file:
        source_content = python_file.read()
        doc_dict = extract_documents(source_content)

    retcode = 0

    for doc_id, doc in doc_dict.items():
        if args.list:
            # try to use default filename when no testcase/doc id is used
            if doc_id is None and args.default_filename is not None:
                doc_id = args.default_filename
            print("{0}".format(doc_id))
            continue
        # report all errors found so far
        for lineno, error in doc.errors():
            msg = "Error on line {0:d}: {1:s} (doc_id: {2:s})"
            print(msg.format(lineno, error, doc_id), file=sys.stderr)
        # TODO: try except
        rst_document = doc.recreate()
        # report all runtime errors
        for error in doc.errors_lastrecreate():
            msg = "Error: {0:s} (doc_id: {1:s})"
            print(msg.format(error, doc_id), file=sys.stderr)
        if args.enforce_id and doc_id is None:
            msg = "docstring without id found while id enforcing enabled"
            # TODO: report line numbers of such docstrings
            print("Error: {0:s}".format(msg), file=sys.stderr)
            retcode = 1
            break
        if args.create_files:
            # try to use default filename when no testcase/doc id is used
            if doc_id is None:
                if args.default_filename is not None:
                    doc_id = args.default_filename
                else:
                    msg = "default filename not specified, skipping 1 document"
                    print("Error: " + msg, file=sys.stderr)
                    retcode = 1
                    continue
            # TODO: change or allow to redefine naming scheme
            filename = "{0}.rst".format(doc_id)
            if args.basedir is not None:
                filepath = os.path.join(args.basedir, filename)
            else:
                filepath = filename
            with open(filepath, 'w') as rst_file:
                rst_file.write(rst_document)
        else:
            print(rst_document, end='')
            if len(doc_dict) > 1:
                print()
        if doc.has_errors():
            retcode = 1

    return retcode
