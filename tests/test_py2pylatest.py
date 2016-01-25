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


class TestStringExtraction(unittest.TestCase):
    """
    Test an extraction of pylatest string literals from python source files.
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
            self.assertEqual(pysource.is_pylatest_docstring(docstring), False)


class TestPylatestDocumentExtraction(unittest.TestCase):
    """
    Test extraction of entire pylatest document from single python source file.

    Input data (python source files) and expected output (pylatest rst file)
    are stored in ``./py2pylatest`` directory.
    """

    def setUp(self):
        # show full diff (note: python3 unittest diff is much better)
        self.maxDiff = None
        # commons steps required for all test cases
        pylatest.client.register_plain()
        self.doc = pysource.PylatestDocument()

    def _read_file(self, name):
        filename = os.path.join(
            HERE, "py2pylatest", "testcase.{0}".format(name))
        with open(filename, 'r') as python_file:
            content = python_file.read()
        return content

    def _test_load_pysource_noerrors(self, testname):
        source = self._read_file(testname)
        expected_result = self._read_file("rst")
        self.doc.load_pysource(source)
        self.assertEqual(len(list(self.doc.errors())), 0)
        self.assertEqual(self.doc.recreate(), expected_result)
        self.assertEqual(len(list(self.doc.errors_lastrecreate())), 0)
        self.assertFalse(self.doc.has_errors())

    def _test_load_pysource_mangled(self, testname, resultname):
        source = self._read_file(testname)
        expected_result = self._read_file(resultname)
        self.doc.load_pysource(source)
        self.assertEqual(self.doc.recreate(), expected_result)
        self.assertTrue(self.doc.has_errors())

    def test_load_pysource_null(self):
        source = self._read_file("null.py")
        self.doc.load_pysource(source)
        self.assertEqual(self.doc.recreate(), "")
        self.assertEqual(len(list(self.doc.errors())), 0)
        self.assertEqual(len(list(self.doc.errors_lastrecreate())), 0)
        self.assertFalse(self.doc.has_errors())

    def test_load_pysource_single(self):
        self._test_load_pysource_noerrors("single.py")

    def test_load_pysource_splitted(self):
        self._test_load_pysource_noerrors("splitted.py")

    def test_load_pysource_splitted_stepsjoined(self):
        self._test_load_pysource_noerrors("splitted-stepsjoined.py")

    def test_load_pysource_splitted_nested(self):
        self._test_load_pysource_noerrors("splitted-nested.py")

    def test_load_pysource_splitted_nested_randomorder(self):
        self._test_load_pysource_noerrors("splitted-nested-randomorder.py")

    def test_load_pysource_single_setupmissing(self):
        self._test_load_pysource_mangled(
            "single-setupmissing.py", "setupmissing.rst")

    def test_load_pysource_single_stepsmissing(self):
        self._test_load_pysource_mangled(
            "single-stepsmissing.py", "stepsmissing.rst")

    def test_load_pysource_single_stepsmissing_teardownmissing(self):
        self._test_load_pysource_mangled(
            "single-stepsmissing-teardownmissing.py",
            "stepsmissing-teardownmissing.rst")
