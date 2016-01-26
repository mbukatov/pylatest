# -*- coding: utf8 -*-

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


import unittest
import textwrap
import os

import pylatest.client
import pylatest.pysource as pysource


HERE = os.path.abspath(os.path.dirname(__file__))


def read_file(dirname, name):
    filename = os.path.join(
        HERE, "pysource-{0}".format(dirname), "testcase.{0}".format(name))
    with open(filename, 'r') as python_file:
        content = python_file.read()
    return content


class TestStringExtraction(unittest.TestCase):
    """
    Test an extraction of string literals from python source files.
    """

    def test_get_string_literals_emptysource(self):
        self.assertEqual(pysource.get_string_literals(""), [])

    def test_get_string_literals_nostrings(self):
        source = textwrap.dedent('''\
        # -*- coding: utf8 -*-

        from __future__ import print_function
        import argparse
        import ast
        import inspect
        import sys

        def main():
            parser = argparse.ArgumentParser(
                description='Generate rst testcase description.')
            parser.add_argument(
                "filepath",
                help="path of python source code automating given testcase")
            args = parser.parse_args()

            foobar = "this is not an anynymous string literal"
            print("hello world!")
        ''')
        self.assertEqual(pysource.get_string_literals(source), [])

    def test_get_string_literals_singlestring(self):
        source = textwrap.dedent('''\
        # -*- coding: utf8 -*-

        from __future__ import print_function
        import argparse
        import ast
        import inspect
        import sys

        def main():
            """
            Main function of py2pylatest cli tool.
            """
            parser = argparse.ArgumentParser(
                description='Generate rst testcase description.')
            parser.add_argument(
                "filepath",
                help="path of python source code automating given testcase")
            args = parser.parse_args()
        ''')
        result = pysource.get_string_literals(source)
        self.assertEqual(len(result), 1)
        docstring_item = ("Main function of py2pylatest cli tool.", 12)
        self.assertEqual(result, [docstring_item])

    def test_is_pylatest_docstring_verysimple(self):
        docstring = """@pylatest
        And now something completelly different.
        """
        is_pylatest_str, _, _ = pysource.classify_docstring(docstring)
        self.assertTrue(is_pylatest_str)

    def test_is_pylatest_docstring_verysimple_withidlist(self):
        docstring = """@pylatest foobar 123
        And now something completelly different.
        """
        is_pylatest_str, _, _ = pysource.classify_docstring(docstring)
        self.assertTrue(is_pylatest_str)

    def test_is_pylatest_docstring_teardownsection(self):
        docstring = """@pylatest
        Teardown
        ========

        #. Lorem ipsum dolor sit amet: ``rm -rf /mnt/helloworld``.

        #. Umount and remove ``lv_helloword`` volume.

        #. The end.
        """
        is_pylatest_str, _, _ = pysource.classify_docstring(docstring)
        self.assertTrue(is_pylatest_str)

    def test_is_pylatest_docstring_falsepositive(self):
        docstring1 = "This is just a string "
        docstring2 = """
        Main function of py2pylatest cli tool.
        """
        docstring3 = """
        Generators have a ``Yields`` section instead of a ``Returns`` section.

        Args:
            n (int): The upper limit of the range to generate, from 0 to `n` - 1.

        Yields:
            int: The next number in the range of 0 to `n` - 1.

        Examples:
            Examples should be written in doctest format, and should illustrate how
            to use the function.

            >>> print([i for i in example_generator(4)])
            [0, 1, 2, 3]
        """
        examples = [docstring1, docstring2, docstring3]
        for docstring in examples:
            is_pylatest_str, _, _ = pysource.classify_docstring(docstring)
            self.assertFalse(is_pylatest_str)

    def test_get_doc_id_list_noid(self):
        docstring = """@pylatest  
        And now something completelly different.
        """
        is_pylatest_str, doc_id_list, _ = pysource.classify_docstring(docstring)
        self.assertTrue(is_pylatest_str)
        self.assertEqual(doc_id_list, [])

    def test_get_doc_id_list_someids(self):
        docstring = """@pylatest foo bar 1234
        And now something completelly different.
        """
        is_pylatest_str, doc_id_list, _ = pysource.classify_docstring(docstring)
        self.assertTrue(is_pylatest_str)
        self.assertEqual(doc_id_list, ['foo', 'bar', '1234'])

    def test_get_docstring_content(self):
        docstring = """@pylatest foo bar 1234
        Bicycle Repair Man.
        """
        is_pylatest_str, _, content = pysource.classify_docstring(docstring)
        self.assertTrue(is_pylatest_str)
        self.assertEqual(content, "        Bicycle Repair Man.\n        ")


class TestPylatestDocumentExtractionOneCaseOneFile(unittest.TestCase):
    """
    Test extraction of entire pylatest document from single python source file.

    Input data (python source files) and expected output (pylatest rst file)
    are stored in ``./pysource-onecaseperfile/`` directory.
    """

    def setUp(self):
        # show full diff (note: python3 unittest diff is much better)
        self.maxDiff = None
        # commons steps required for all test cases
        pylatest.client.register_plain()

    def _test_extract_document_noerrors(self, testname):
        source = read_file("onecaseperfile", testname)
        expected_result = read_file("onecaseperfile", "rst")
        doc_dict = pysource.extract_documents(source)
        self.assertEqual(len(doc_dict), 1)
        doc = doc_dict[None]
        self.assertEqual(len(list(doc.errors())), 0)
        self.assertEqual(doc.recreate(), expected_result)
        self.assertEqual(len(list(doc.errors_lastrecreate())), 0)
        self.assertFalse(doc.has_errors())

    def _test_extract_document_mangled(self, testname, resultname):
        source = read_file("onecaseperfile", testname)
        expected_result = read_file("onecaseperfile", resultname)
        doc_dict = pysource.extract_documents(source)
        self.assertEqual(len(doc_dict), 1)
        doc = doc_dict[None]
        self.assertEqual(doc.recreate(), expected_result)
        self.assertTrue(doc.has_errors())

    def test_extract_document_null(self):
        source = read_file("onecaseperfile", "null.py")
        doc_dict = pysource.extract_documents(source)
        self.assertEqual(doc_dict, {})

    def test_extract_document_single(self):
        self._test_extract_document_noerrors("single.py")

    def test_extract_document_splitted(self):
        self._test_extract_document_noerrors("splitted.py")

    def test_extract_document_splitted_stepsjoined(self):
        self._test_extract_document_noerrors("splitted-stepsjoined.py")

    def test_extract_document_splitted_nested(self):
        self._test_extract_document_noerrors("splitted-nested.py")

    def test_extract_document_splitted_nested_randomorder(self):
        self._test_extract_document_noerrors("splitted-nested-randomorder.py")

    def test_extract_document_single_setupmissing(self):
        self._test_extract_document_mangled(
            "single-setupmissing.py", "setupmissing.rst")

    def test_extract_document_single_stepsmissing(self):
        self._test_extract_document_mangled(
            "single-stepsmissing.py", "stepsmissing.rst")

    def test_extract_document_single_stepsmissing_teardownmissing(self):
        self._test_extract_document_mangled(
            "single-stepsmissing-teardownmissing.py",
            "stepsmissing-teardownmissing.rst")


class TestPylatestDocumentsExtractionMultipleCasesPerFile(unittest.TestCase):
    """
    Test extraction of multiple pylatest documents from single python file.

    Input data (python source files) and expected output (pylatest rst files)
    are stored in ``./pysource-multiplecasesperfile/`` directory.
    """

    def setUp(self):
        # show full diff (note: python3 unittest diff is much better)
        self.maxDiff = None
        # common steps required for all test cases
        pylatest.client.register_plain()

    def _test_extract_documents_noerrors(self, doc_num, testname):
        source = read_file("multiplecasesperfile", testname)
        doc_dict = pysource.extract_documents(source)
        self.assertEqual(len(doc_dict), doc_num)
        for doc_id, doc in doc_dict.items():
            filename = "{}.rst".format(doc_id)
            expected_result = read_file("multiplecasesperfile", filename)
            self.assertEqual(len(list(doc.errors())), 0)
            self.assertEqual(doc.recreate(), expected_result)
            self.assertEqual(len(list(doc.errors_lastrecreate())), 0)
            self.assertFalse(doc.has_errors())

    def test_extract_documents_splitted_nested(self):
        self._test_extract_documents_noerrors(2, "splitted-nested.py")
