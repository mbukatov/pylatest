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

from pylatest.document import TestCaseDoc, RstTestCaseDoc, Section
from pylatest.rstsource import find_actions, find_sections
from pylatest.xdocutils.core import register_all


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

def extract_doc_fragments(source):
    """
    Try to extract pylatest document fragments from given string (content of
    a python source file) and generate TestCaseDocFragments objects from it.

    Args:
        source(string): content of a python source file

    Returns:
        dict of TestCaseDocFragments items generated from given python source
    """
    # doc_id (aka testcase id) -> pylatest document fragments object
    docfr_dict = {}
    default_docfr = TestCaseDocFragments()
    for docstring, lineno in get_string_literals(source):
        is_pylatest_str, doc_id_list, content = classify_docstring(docstring)
        if is_pylatest_str:
            if len(doc_id_list) == 0:
                # when no id is detected, create special document without id
                doc_id_list = [None]
            elif "default" in doc_id_list:
                default_docfr.add_fragment(content, lineno)
                continue
            for doc_id in doc_id_list:
                docfr = docfr_dict.setdefault(doc_id, TestCaseDocFragments())
                docfr.add_fragment(content, lineno)
    # allow all document objects to find defaults if needed
    if len(default_docfr) > 0:
        for docfr in docfr_dict.values():
            docfr.default = default_docfr
    return docfr_dict


def extract_content(str_lines, start, end):
    """
    Extract content on given lines (start, end) from str_lines list and return
    it as a single string.
    """
    return "\n".join(str_lines[start - 1:end]) + '\n'


class TestCaseDocFragments(object):
    """
    Pylatest strings of with a test case description extracted from python
    source code (implementing the test case).
    """

    def __init__(self):
        # TODO: rename
        self.docstrings = {}
        """
        List of docstrings with at least one section, line number -> string
        """

        self.default = None
        """
        Document Fragments object with default content
        """

        # TODO: set to a proper value
        self.source_file = ""
        """
        Name of the source file from which this string literal (doc fragment)
        has been extracted.
        """

    def __len__(self):
        return len(self.docstrings)

    def add_fragment(self, docstring, lineno):
        """
        Args:
            docstring (str): content of single docstring expression
            lineno (int): line number of the docstring
        """
        # TODO: also, why do I store the lineno like this?
        self.docstrings[lineno] = docstring

    def build_doc(self):
        """
        Build RstTestCaseDoc object based on pylatest string literals (aka
        document fragments) stored in this object.
        """
        if self.default is None:
            doc = RstTestCaseDoc()
        else:
            # TODO: this builds the default doc every time, cache the build
            # (if nothing changed - for merging def doc.)
            doc = self.default.build_doc()
        # find pylatest document sections/directives in every fragment
        for lineno, doc_str in self.docstrings.items():
            doc_str_lines = doc_str.splitlines()
            for rst_act in find_actions(doc_str):
                content = extract_content(
                    doc_str_lines, rst_act.start_line, rst_act.end_line)
                doc.add_test_action(
                    rst_act.action_name,
                    content,
                    rst_act.action_id,
                    lineno)
            for rst_sct in find_sections(doc_str):
                if rst_sct.title is None:
                    section = TestCaseDoc._HEAD
                else:
                    section = Section(rst_sct.title)
                content = extract_content(
                    doc_str_lines, rst_sct.start_line, rst_sct.end_line)
                doc.add_section(section, content, lineno)
        return doc


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
    register_all(use_plain=True)

    with open(args.filepath, 'r') as python_file:
        source_content = python_file.read()
        docfr_dict = extract_doc_fragments(source_content)

    retcode = 0

    for doc_id, doc_fr in docfr_dict.items():
        if args.list:
            # here we list test case names wihtout doing anything else
            # try to use default filename as a testcase name (aka doc id)
            # when doc id is not specified
            if doc_id is None and args.default_filename is not None:
                doc_id = args.default_filename
            print("{0}".format(doc_id))
            continue

        # TODO: add proper error checking
        # build RstTestCaseDoc from TestCaseDocFragments
        doc = doc_fr.build_doc()
        # generate string with rst source for the test case document
        rst_content = doc.build_rst()

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
                rst_file.write(rst_content)
        else:
            print(rst_content, end='')
            if len(docfr_dict) > 1:
                print()

    return retcode
