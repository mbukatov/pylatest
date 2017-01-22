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

from pylatest.document import TestCaseDoc
import pylatest.pysource as pysource
import pylatest.xdocutils.client


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


class TestTestCaseDocFragments(unittest.TestCase):
    """
    Tests of pylatest.pysource.TestCaseDocFragments class.
    """

    def setUp(self):
        pylatest.xdocutils.client.register_plain()
        self.fragments = pysource.TestCaseDocFragments()

    def test_docfragments_null(self):
        self.assertEqual(len(self.fragments), 0)
        self.assertIsNone(self.fragments.default)

    def test_docfragments_add_one(self):
        self.fragments.add_fragment("foo bar baz", 11)
        self.assertEqual(len(self.fragments), 1)
        self.assertIsNone(self.fragments.default)
        self.assertEqual(self.fragments.docstrings.get(11), "foo bar baz")

    def test_docfragments_add_few(self):
        self.fragments.add_fragment("foo", 1)
        self.assertEqual(len(self.fragments), 1)
        self.assertIsNone(self.fragments.default)
        for i in range(10):
            self.fragments.add_fragment("just another_one", i + 10)
        self.assertEqual(len(self.fragments), 11)
        self.assertIsNone(self.fragments.default)

    def test_docfragments_build_doc_empty(self):
        doc = self.fragments.build_doc()
        self.assertTrue(doc.is_empty())

    def test_docfragments_build_doc_singlestep(self):
        str_fragment = textwrap.dedent('''\
        .. test_step:: 1

            List files in the volume: ``ls -a /mnt/helloworld``
        ''')
        self.fragments.add_fragment(str_fragment, lineno=11)
        doc = self.fragments.build_doc()
        self.assertFalse(doc.is_empty())
        self.assertTrue(TestCaseDoc.STEPS in doc.sections)

    def test_docfragments_build_doc_multiple(self):
        fragment_one = textwrap.dedent('''\
        .. test_step:: 1

            List files in the volume: ``ls -a /mnt/helloworld``
        ''')
        fragment_two = textwrap.dedent('''\
        Hello World Test Case
        *********************

        .. test_metadata:: author foo@example.com
        .. test_metadata:: date 2015-11-06

        Description
        ===========

        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec a diam
        lectus.  Sed sit amet ipsum mauris. Maecenas congue ligula ac quam

        Teardown
        ========

        #. Lorem ipsum dolor sit amet: ``rm -rf /mnt/helloworld``.
        ''')
        self.fragments.add_fragment(fragment_one, lineno=11)
        self.fragments.add_fragment(fragment_two, lineno=131)
        doc = self.fragments.build_doc()
        self.assertFalse(doc.is_empty())
        self.assertTrue(TestCaseDoc._HEAD in doc.sections)
        self.assertTrue(TestCaseDoc.DESCR in doc.sections)
        self.assertTrue(TestCaseDoc.STEPS in doc.sections)
        self.assertTrue(TestCaseDoc.TEARD in doc.sections)


class TestExtractDocumentFragments(unittest.TestCase):
    """
    Test extraction of pylatest document fragments (pylatest string literals)
    from python source file - function ``pysource.extract_doc_fragments``

    Input data (python source files) and expected output (pylatest rst file)
    are stored in ``./pysource-onecaseperfile/`` directory.
    """

    def setUp(self):
        # show full diff (note: python3 unittest diff is much better)
        self.maxDiff = None
        # commons steps required for all test cases
        pylatest.xdocutils.client.register_plain()

    def test_extract_doc_fragments_null_str(self):
        doc_fragment_dict = pysource.extract_doc_fragments("")
        self.assertEqual(len(doc_fragment_dict), 0)
        self.assertEqual(doc_fragment_dict, {})

    def test_extract_doc_fragments_null(self):
        source = read_file("onecaseperfile", "null.py")
        doc_fragment_dict = pysource.extract_doc_fragments(source)
        self.assertEqual(len(doc_fragment_dict), 0)
        self.assertEqual(doc_fragment_dict, {})

    def test_extract_doc_fragments_onecaseperfile_single(self):
        source = read_file("onecaseperfile", "single.py")
        doc_fragment_dict = pysource.extract_doc_fragments(source)
        self.assertEqual(len(doc_fragment_dict), 1)
        doc_fragments = doc_fragment_dict[None]
        self.assertEqual(len(doc_fragments), 1)
        self.assertIsNone(doc_fragments.default)

    def test_extract_doc_fragments_onecaseperfile_splitted_nested(self):
        source = read_file("onecaseperfile", "splitted-nested.py")
        doc_fragment_dict = pysource.extract_doc_fragments(source)
        # there is just a single test case in the file
        # (as 'onecaseperfile' directory name suggests)
        self.assertEqual(len(doc_fragment_dict), 1)
        # pylatest strings are without pylatest ids
        doc_fragments = doc_fragment_dict[None]
        # there are 9 pylatest strings in given file
        self.assertEqual(len(doc_fragments), 9)
        # the default doc feature is not used in given file
        self.assertIsNone(doc_fragments.default)
        # pylatest string literal which ends on line 95 in splitted-neste.py file
        fragment_line95 = textwrap.dedent('''\
        .. test_step:: 1

            List files in the volume: ``ls -a /mnt/helloworld``''')
        self.assertEqual(doc_fragments.docstrings[95], fragment_line95)

    def test_extract_doc_fragments_multiplecasesperfile_splitted_nested(self):
        source = read_file("multiplecasesperfile", "splitted-nested.py")
        doc_fragment_dict = pysource.extract_doc_fragments(source)
        self.assertEqual(len(doc_fragment_dict), 2)
        # number of expected pylatest strings for each pylatest doc id
        expected_fragments = {
            'test01': 9,
            'test02': 7,
            }
        for doc_id, doc_fragments in doc_fragment_dict.items():
            # default doc feature is not used in the file
            self.assertIsNone(doc_fragments.default)
            # check expected number of pylatest strings
            self.assertEqual(len(doc_fragments), expected_fragments[doc_id])
        # check that some pylatest strings are the same in both doc fragments
        for linenum in (77, 96):
            self.assertEqual(
                doc_fragment_dict['test01'].docstrings[linenum],
                doc_fragment_dict['test02'].docstrings[linenum],)

    def test_extract_documents_splitted_nested_withdefault(self):
        source = read_file("multiplecasesperfile", "splitted-nested-default.py")
        doc_fragment_dict = pysource.extract_doc_fragments(source)
        self.assertEqual(len(doc_fragment_dict), 2)
        for doc_id, doc_fragments in doc_fragment_dict.items():
            # default doc is used in the file (for setup and teardown strings)
            self.assertIsNotNone(doc_fragments.default)
            self.assertEqual(len(doc_fragments.default), 2)


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
        pylatest.xdocutils.client.register_plain()

    def _test_extract_document_noerrors(self, testname):
        source = read_file("onecaseperfile", testname)
        expected_result = read_file("onecaseperfile", "rst")
        # extract TestCaseDocFragments from the python source file
        docfr_dict = pysource.extract_doc_fragments(source)
        # there should be just one test case document
        self.assertEqual(len(docfr_dict), 1)
        # this document is without pylatest id
        doc_fr = docfr_dict[None]
        # then build RstTestCaseDoc from TestCaseDocFragments
        doc = doc_fr.build_doc()
        # and finally build the rst source version
        self.assertEqual(doc.build_rst(), expected_result)

    def _test_extract_document_mangled(self, testname, resultname):
        source = read_file("onecaseperfile", testname)
        expected_result = read_file("onecaseperfile", resultname)
        # extract TestCaseDocFragments from the python source file
        docfr_dict = pysource.extract_doc_fragments(source)
        # there should be just one test case document
        self.assertEqual(len(docfr_dict), 1)
        # this document is without pylatest id
        doc_fr = docfr_dict[None]
        # TODO: needs update to work with new error handling (not yet done)
        # then build RstTestCaseDoc from TestCaseDocFragments
        doc = doc_fr.build_doc()
        # and finally build the rst source version
        self.assertEqual(doc.build_rst(), expected_result)

    def test_extract_document_null(self):
        source = read_file("onecaseperfile", "null.py")
        docfr_dict = pysource.extract_doc_fragments(source)
        self.assertEqual(docfr_dict, {})

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

    def test_extract_document_single_descriptionmissing(self):
        self._test_extract_document_mangled(
            "single-descriptionmissing.py", "descriptionmissing.rst")

    def test_extract_document_single_descriptionmissing_setupmissing(self):
        self._test_extract_document_mangled(
            "single-descriptionmissing-setupmissing.py",
            "descriptionmissing-setupmissing.rst")

    def test_extract_document_single_stepsmissing_teardownmissing(self):
        self._test_extract_document_mangled(
            "single-stepsmissing-teardownmissing.py",
            "stepsmissing-teardownmissing.rst")

    def test_extract_document_splitted_descriptionmissing(self):
        self._test_extract_document_mangled(
            "splitted-descriptionmissing.py", "descriptionmissing.rst")

    def test_extract_document_splitted_setupmissing(self):
        self._test_extract_document_mangled(
            "splitted-setupmissing.py", "setupmissing.rst")


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
        pylatest.xdocutils.client.register_plain()

    def _test_extract_documents_noerrors(self, doc_num, testname):
        # TODO: needs update to work with new error handling (not yet done)
        source = read_file("multiplecasesperfile", testname)
        # extract TestCaseDocFragments from the python source file
        docfr_dict = pysource.extract_doc_fragments(source)
        self.assertEqual(len(docfr_dict), doc_num)
        for doc_id, doc_fr in docfr_dict.items():
            if doc_id is None:
                doc_id = "none"
            filename = "{}.rst".format(doc_id)
            expected_result = read_file("multiplecasesperfile", filename)
            # build RstTestCaseDoc from TestCaseDocFragments
            doc = doc_fr.build_doc()
            self.assertEqual(doc.build_rst(), expected_result)

    def test_extract_documents_splitted_nested(self):
        self._test_extract_documents_noerrors(2, "splitted-nested.py")

    def test_extract_documents_splitted_nested_withdefault(self):
        self._test_extract_documents_noerrors(2, "splitted-nested-default.py")

    def test_extract_documents_splitted_nested_withdefault_override(self):
        pyfilename = "splitted-nested-default-override.py"
        self._test_extract_documents_noerrors(3, pyfilename)

    def test_extract_documents_splitted_nested_withdefault_override_null(self):
        pyfilename = "splitted-nested-default-override-null.py"
        self._test_extract_documents_noerrors(3, pyfilename)
