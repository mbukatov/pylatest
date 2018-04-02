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
import sys
import codecs

from pylatest.document import TestCaseDoc
import pylatest.pysource as pysource
import pylatest.xdocutils.core


HERE = os.path.abspath(os.path.dirname(__file__))


def read_file(dirname, name):
    filename = os.path.join(
        HERE, "pysource-{0}".format(dirname), "testcase.{0}".format(name))
    if sys.version_info[0] == 2:
        # python compat hack: python2 ast module can't handle unicode input
        # for some reason (so that codecs.open() can't be used here)
        with open(filename, 'r') as python_file:
            content = python_file.read()
    else:
        # specify encoding properly so that it would work with LC_ALL=C
        # for more details, see python3 and locale.getpreferredencoding
        with codecs.open(filename, 'r', encoding='utf8') as python_file:
            content = python_file.read()
    return content


class TestStringExtraction(unittest.TestCase):
    """
    Test an extraction of string literals from python source files.
    """

    def test_get_string_literals_emptysource(self):
        assert pysource.get_string_literals("") == []

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
        assert pysource.get_string_literals(source) == []

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
        assert len(result) == 1
        docstring_item = ("Main function of py2pylatest cli tool.", 12)
        assert result == [docstring_item]

    def test_is_pylatest_docstring_verysimple(self):
        docstring = """@pylatest
        And now something completelly different.
        """
        is_pylatest_str, _, _ = pysource.classify_docstring(docstring)
        assert is_pylatest_str

    def test_is_pylatest_docstring_verysimple_withidlist(self):
        docstring = """@pylatest foobar 123
        And now something completelly different.
        """
        is_pylatest_str, _, _ = pysource.classify_docstring(docstring)
        assert is_pylatest_str

    def test_is_pylatest_docstring_teardownsection(self):
        docstring = """@pylatest
        Teardown
        ========

        #. Lorem ipsum dolor sit amet: ``rm -rf /mnt/helloworld``.

        #. Umount and remove ``lv_helloword`` volume.

        #. The end.
        """
        is_pylatest_str, _, _ = pysource.classify_docstring(docstring)
        assert is_pylatest_str

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
            assert not is_pylatest_str

    def test_get_doc_id_list_noid(self):
        docstring = """@pylatest  
        And now something completelly different.
        """
        is_pylatest_str, doc_id_list, _ = pysource.classify_docstring(docstring)
        assert is_pylatest_str
        assert doc_id_list == []

    def test_get_doc_id_list_someids(self):
        docstring = """@pylatest foo bar 1234
        And now something completelly different.
        """
        is_pylatest_str, doc_id_list, _ = pysource.classify_docstring(docstring)
        assert is_pylatest_str
        assert doc_id_list == ['foo', 'bar', '1234']

    def test_get_docstring_content(self):
        docstring = """@pylatest foo bar 1234
        Bicycle Repair Man.
        """
        is_pylatest_str, _, content = pysource.classify_docstring(docstring)
        assert is_pylatest_str
        assert content == "        Bicycle Repair Man.\n        "


class TestTestCaseDocFragments(unittest.TestCase):
    """
    Tests of pylatest.pysource.TestCaseDocFragments class.
    """

    def setUp(self):
        pylatest.xdocutils.core.register_all(use_plain=True)
        self.fragments = pysource.TestCaseDocFragments()

    def test_docfragments_null(self):
        assert len(self.fragments) == 0
        assert self.fragments.default is None

    def test_docfragments_add_one(self):
        self.fragments.add_fragment("foo bar baz", 11)
        assert len(self.fragments) == 1
        assert self.fragments.default is None
        assert self.fragments.docstrings.get(11) == "foo bar baz"

    def test_docfragments_add_few(self):
        self.fragments.add_fragment("foo", 1)
        assert len(self.fragments) == 1
        assert self.fragments.default is None
        for i in range(10):
            self.fragments.add_fragment("just another_one", i + 10)
        assert len(self.fragments) == 11
        assert self.fragments.default is None

    def test_docfragments_build_doc_empty(self):
        doc = self.fragments.build_doc()
        assert doc.is_empty()

    def test_docfragments_build_doc_singlestep(self):
        str_fragment = textwrap.dedent('''\
        .. test_step:: 1

            List files in the volume: ``ls -a /mnt/helloworld``
        ''')
        self.fragments.add_fragment(str_fragment, lineno=11)
        doc = self.fragments.build_doc()
        assert not doc.is_empty()
        assert TestCaseDoc.STEPS in doc.sections

    def test_docfragments_build_doc_multiple(self):
        fragment_one = textwrap.dedent('''\
        .. test_step:: 1

            List files in the volume: ``ls -a /mnt/helloworld``
        ''')
        fragment_two = textwrap.dedent('''\
        Hello World Test Case
        *********************

        :author: foo@example.com
        :date: 2015-11-06

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
        assert not doc.is_empty()
        assert TestCaseDoc._HEAD in doc.sections
        assert TestCaseDoc.DESCR in doc.sections
        assert TestCaseDoc.STEPS in doc.sections
        assert TestCaseDoc.TEARD in doc.sections

    def test_docfragments_build_doc_section_header(self):
        fragment = textwrap.dedent('''\
        Just Another Test Case
        **********************

        :author: foo.bar@example.com

        Description
        ===========

        Vivamus fermentum semper porta. Nunc diam velit, adipiscing ut tristique
        vitae, sagittis vel odio. Maecenas convallis ullamcorper ultricies.
        ''')
        expected_head = textwrap.dedent('''\
        Just Another Test Case
        **********************

        :author: foo.bar@example.com
        ''')
        expected_desc = textwrap.dedent('''\
        Description
        ===========

        Vivamus fermentum semper porta. Nunc diam velit, adipiscing ut tristique
        vitae, sagittis vel odio. Maecenas convallis ullamcorper ultricies.
        ''')
        self.fragments.add_fragment(fragment, lineno=133)
        doc = self.fragments.build_doc()
        assert not doc.is_empty()
        assert TestCaseDoc._HEAD in doc.sections
        assert TestCaseDoc.DESCR in doc.sections
        assert doc.get_section(TestCaseDoc._HEAD) == expected_head
        assert doc.get_section(TestCaseDoc.DESCR) == expected_desc

    def test_docfragments_build_doc_section_override(self):
        # 1st fragment
        fragment_one = textwrap.dedent('''\
        Just Another Test Case
        **********************

        :author: foo.bar@example.com

        Description
        ===========

        Vivamus fermentum semper porta. Nunc diam velit, adipiscing ut tristique
        vitae, sagittis vel odio. Maecenas convallis ullamcorper ultricies.
        Curabitur ornare, ligula semper consectetur sagittis, nisi diam iaculis
        velit, id fringilla sem nunc vel mi. Nam dictum, odio nec pretium volutpat,
        arcu ante placerat erat, non tristique elit urna et turpis.
        ''')
        # header from 1st fragment
        expected_head_one = textwrap.dedent('''\
        Just Another Test Case
        **********************

        :author: foo.bar@example.com
        ''')
        # description section from 1st fragment
        expected_desc_one = textwrap.dedent('''\
        Description
        ===========

        Vivamus fermentum semper porta. Nunc diam velit, adipiscing ut tristique
        vitae, sagittis vel odio. Maecenas convallis ullamcorper ultricies.
        Curabitur ornare, ligula semper consectetur sagittis, nisi diam iaculis
        velit, id fringilla sem nunc vel mi. Nam dictum, odio nec pretium volutpat,
        arcu ante placerat erat, non tristique elit urna et turpis.
        ''')
        # 2nd fragment and expected description section after update
        fragment_two = textwrap.dedent('''\
        Description
        ===========

        This is just demonstration of usage of pylatest rst directives and expected
        structure of rst document.

        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec a diam lectus.
        Sed sit amet ipsum mauris. Maecenas congue ligula ac quam viverra nec
        consectetur ante hendrerit. Donec et mollis dolor. Praesent et diam eget libero
        egestas mattis sit amet vitae augue.

        See :RHBZ:`439858` for more details.
        ''')
        # process 1st fragment first
        self.fragments.add_fragment(fragment_one, lineno=131)
        doc1 = self.fragments.build_doc()
        assert not doc1.is_empty()
        assert TestCaseDoc._HEAD in doc1.sections
        assert TestCaseDoc.DESCR in doc1.sections
        assert doc1.get_section(TestCaseDoc._HEAD) == expected_head_one
        assert doc1.get_section(TestCaseDoc.DESCR) == expected_desc_one
        # update: add 2nd fragment and retry
        # note: override feature works only wrt default document
        fragments2 = pysource.TestCaseDocFragments()
        fragments2.default = self.fragments
        fragments2.add_fragment(fragment_two, lineno=11)
        doc2 = fragments2.build_doc()
        assert not doc2.is_empty()
        assert TestCaseDoc._HEAD in doc2.sections
        assert TestCaseDoc.DESCR in doc2.sections
        assert doc2.get_section(TestCaseDoc._HEAD) == expected_head_one
        assert doc2.get_section(TestCaseDoc.DESCR) == fragment_two

    def test_docfragments_build_doc_multiple_buildmany(self):
        fragment_one = textwrap.dedent('''\
        .. test_step:: 1

            List files in the volume: ``ls -a /mnt/helloworld``
        ''')
        fragment_two = textwrap.dedent('''\
        Hello World Test Case
        *********************

        :author: foo@example.com
        :date: 2015-11-06

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
        # buil few docs from the fragments
        doc1 = self.fragments.build_doc()
        doc2 = self.fragments.build_doc()
        doc3 = self.fragments.build_doc()
        # every build should be independent and lead the the same result
        assert doc1 == doc2
        assert doc2 == doc3

    def test_docfragments_build_doc_multiple_fragmented(self):
        rst_fragments = [
            textwrap.dedent("""\
            Hello World Test Case
            *********************

            :author: foo@example.com
            :date: 2015-11-06
            :comment: This is here just to test metadata processing.
            """),
            textwrap.dedent("""\
            Description
            ===========

            This is just demonstration of usage of pylatest rst directives and expected
            structure of rst document.

            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec a diam lectus.
            Sed sit amet ipsum mauris. Maecenas congue ligula ac quam viverra nec
            consectetur ante hendrerit. Donec et mollis dolor. Praesent et diam eget libero
            egestas mattis sit amet vitae augue.

            See :RHBZ:`439858` for more details.
            """),
            textwrap.dedent("""\
            .. test_step:: 1

                List files in the volume: ``ls -a /mnt/helloworld``
            """),
            textwrap.dedent("""\
            .. test_result:: 1

                There are no files, output should be empty.
            """),
            textwrap.dedent("""\
            .. test_step:: 2

                Donec et mollis dolor::

                    $ foo --extra sth
                    $ bar -vvv
            """),
            textwrap.dedent("""\
            .. test_result:: 2

                Maecenas congue ligula ac quam viverra nec
                consectetur ante hendrerit.
            """),
            textwrap.dedent("""\
            .. test_step:: 3

                This one has no matching test result.
            """),
            textwrap.dedent("""\
            .. test_result:: 4

                And this result has no test step.
            """),
            textwrap.dedent("""\
            Setup
            =====

            #. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec a diam
               lectus. Sed sit amet ipsum mauris.

            #. Use lvm disk paritioning and Leave 10G free space in volume
               called ``lv_helloword``.

            #. When the system is installed, format ``lv_helloword`` volume with
               brtfs using ``--super --special --options``.

            #. Mount it on a client::

                # mount -t btrfs /dev/mapper/vg_fedora/lv_helloword /mnt/helloworld

            #. Ceterum censeo, lorem ipsum::

                # dnf install foobar
                # systemctl enable foobard
            """),
            textwrap.dedent("""\
            Teardown
            ========

            #. Lorem ipsum dolor sit amet: ``rm -rf /mnt/helloworld``.

            #. Umount and remove ``lv_helloword`` volume.

            #. The end.
            """),
            ]
        for index, fragment in enumerate(rst_fragments):
            # line number have to be unique
            lineno = index*100 + 2
            self.fragments.add_fragment(fragment, lineno=lineno)
        assert len(self.fragments) == len(rst_fragments)
        doc = self.fragments.build_doc()
        assert not doc.is_empty()
        assert TestCaseDoc.DESCR in doc.sections
        assert TestCaseDoc.SETUP in doc.sections
        assert TestCaseDoc.STEPS in doc.sections
        assert TestCaseDoc.TEARD in doc.sections
        assert TestCaseDoc._HEAD in doc.sections


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
        pylatest.xdocutils.core.register_all(use_plain=True)

    def test_extract_doc_fragments_null_str(self):
        doc_fragment_dict = pysource.extract_doc_fragments("")
        assert len(doc_fragment_dict) == 0
        assert doc_fragment_dict == {}

    def test_extract_doc_fragments_null(self):
        source = read_file("onecaseperfile", "null.py")
        doc_fragment_dict = pysource.extract_doc_fragments(source)
        assert len(doc_fragment_dict) == 0
        assert doc_fragment_dict == {}

    def test_extract_doc_fragments_onecaseperfile_single(self):
        source = read_file("onecaseperfile", "single.py")
        doc_fragment_dict = pysource.extract_doc_fragments(source)
        assert len(doc_fragment_dict) == 1
        doc_fragments = doc_fragment_dict[None]
        assert len(doc_fragments) == 1
        assert doc_fragments.default is None

    def test_extract_doc_fragments_onecaseperfile_splitted_nested(self):
        source = read_file("onecaseperfile", "splitted-nested.py")
        doc_fragment_dict = pysource.extract_doc_fragments(source)
        # there is just a single test case in the file
        # (as 'onecaseperfile' directory name suggests)
        assert len(doc_fragment_dict) == 1
        # pylatest strings are without pylatest ids
        doc_fragments = doc_fragment_dict[None]
        # there are 9 pylatest strings in given file
        assert len(doc_fragments) == 9
        # the default doc feature is not used in given file
        assert doc_fragments.default is None
        # pylatest string literal which ends on line 95 in splitted-neste.py file
        fragment_line95 = textwrap.dedent('''\
        .. test_step:: 1

            List files in the volume: ``ls -a /mnt/helloworld``''')
        assert doc_fragments.docstrings[95] == fragment_line95

    def test_extract_doc_fragments_multiplecasesperfile_splitted_nested(self):
        source = read_file("multiplecasesperfile", "splitted-nested.py")
        doc_fragment_dict = pysource.extract_doc_fragments(source)
        assert len(doc_fragment_dict) == 2
        # number of expected pylatest strings for each pylatest doc id
        expected_fragments = {
            'test01': 9,
            'test02': 7,
            }
        for doc_id, doc_fragments in doc_fragment_dict.items():
            # default doc feature is not used in the file
            assert doc_fragments.default is None
            # check expected number of pylatest strings
            assert len(doc_fragments) == expected_fragments[doc_id]
        # check that some pylatest strings are the same in both doc fragments
        for linenum in (77, 96):
            assert doc_fragment_dict['test01'].docstrings[linenum] == \
                   doc_fragment_dict['test02'].docstrings[linenum]

    def test_extract_documents_splitted_nested_withdefault(self):
        source = read_file("multiplecasesperfile", "splitted-nested-default.py")
        doc_fragment_dict = pysource.extract_doc_fragments(source)
        assert len(doc_fragment_dict) == 2
        for doc_id, doc_fragments in doc_fragment_dict.items():
            # default doc is used in the file (for setup and teardown strings)
            assert doc_fragments.default is not None
            assert len(doc_fragments.default) == 2


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
        pylatest.xdocutils.core.register_all(use_plain=True)

    def _test_extract_document_noerrors(self, testname):
        source = read_file("onecaseperfile", testname)
        expected_result = read_file("onecaseperfile", "rst")
        # extract TestCaseDocFragments from the python source file
        docfr_dict = pysource.extract_doc_fragments(source)
        # there should be just one test case document
        assert len(docfr_dict) == 1
        # this document is without pylatest id
        doc_fr = docfr_dict[None]
        # then build RstTestCaseDoc from TestCaseDocFragments
        doc = doc_fr.build_doc()
        # and finally build the rst source version
        assert doc.build_rst() == expected_result
        # every build should be the same
        assert doc.build_rst() == expected_result

    def _test_extract_document_mangled(self, testname, resultname):
        source = read_file("onecaseperfile", testname)
        expected_result = read_file("onecaseperfile", resultname)
        # extract TestCaseDocFragments from the python source file
        docfr_dict = pysource.extract_doc_fragments(source)
        # there should be just one test case document
        assert len(docfr_dict) == 1
        # this document is without pylatest id
        doc_fr = docfr_dict[None]
        # TODO: needs update to work with new error handling (not yet done)
        # then build RstTestCaseDoc from TestCaseDocFragments
        doc = doc_fr.build_doc()
        # and finally build the rst source version
        assert doc.build_rst() == expected_result
        # every build should be the same
        assert doc.build_rst() == expected_result

    def test_extract_document_null(self):
        source = read_file("onecaseperfile", "null.py")
        docfr_dict = pysource.extract_doc_fragments(source)
        assert docfr_dict == {}

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
        pylatest.xdocutils.core.register_all(use_plain=True)

    def _test_extract_documents_noerrors(self, doc_num, testname):
        # TODO: needs update to work with new error handling (not yet done)
        source = read_file("multiplecasesperfile", testname)
        # extract TestCaseDocFragments from the python source file
        docfr_dict = pysource.extract_doc_fragments(source)
        assert len(docfr_dict) == doc_num
        for doc_id, doc_fr in docfr_dict.items():
            if doc_id is None:
                doc_id = "none"
            filename = "{}.rst".format(doc_id)
            expected_result = read_file("multiplecasesperfile", filename)
            # build RstTestCaseDoc from TestCaseDocFragments
            doc = doc_fr.build_doc()
            assert doc.build_rst() == expected_result
            # every build should be the same
            assert doc.build_rst() == expected_result

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
