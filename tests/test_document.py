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

import pytest
from lxml import etree

from pylatest.document import Section, TestCaseDoc, RstTestCaseDoc
from pylatest.document import XmlExportTestCaseDoc
import pylatest.document


class TestTestActions(unittest.TestCase):
    """
    Tests of pylatest.document.TestActions class.
    """

    def setUp(self):
        self.actions = pylatest.document.TestActions()

    def test_actions_null(self):
        assert len(self.actions) == 0

    def test_actions_iter_null(self):
        assert list(self.actions) == []
        assert list(self.actions.iter_content()) == []

    def test_actions_add_onefull(self):
        self.actions.add("test_step", "1.step", 1)
        assert len(self.actions) == 1
        self.actions.add("test_result", "1.result", 1)
        assert len(self.actions) == 1
        assert list(self.actions.iter_content()) == ["1.step", "1.result"]
        assert list(self.actions) == [(1, '1.step', '1.result')]

    def test_actions_add_error(self):
        with pytest.raises(pylatest.document.PylatestActionsError):
            self.actions.add("test_foobar", "1.foobar", 1)
        assert len(self.actions) == 0

    def test_actions_add_onestep(self):
        self.actions.add("test_step", "1.step", 1)
        assert len(self.actions) == 1
        assert list(self.actions.iter_content()) == ["1.step"]
        assert list(self.actions) == [(1, '1.step', None)]

    def test_actions_add_oneresult(self):
        self.actions.add("test_result", "1.result", 1)
        assert len(self.actions) == 1
        assert list(self.actions.iter_content()) == ["1.result"]
        assert list(self.actions) == [(1, None, '1.result')]

    def test_actions_add_result(self):
        self.actions.add_result("1.result", 1)
        assert len(self.actions) == 1
        assert list(self.actions.iter_content()) == ["1.result"]
        assert list(self.actions) == [(1, None, '1.result')]

    def test_actions_add_step(self):
        self.actions.add_step("1.step", 1)
        assert len(self.actions) == 1
        assert list(self.actions.iter_content()) == ["1.step"]
        assert list(self.actions) == [(1, '1.step', None)]

    def test_actions_add_clash_enforce_id_false(self):
        self.actions = pylatest.document.TestActions(enforce_id=False)
        self.actions.add("test_step", "1.step-1", 1)
        self.actions.add("test_result", "1.result", 1)
        assert len(self.actions) == 1
        self.actions.add("test_step", "1.step-2", 1)
        assert len(self.actions) == 1
        assert list(self.actions.iter_content()) == ["1.step-2", "1.result"]
        assert list(self.actions) == [(1, '1.step-2', '1.result')]

    def test_actions_add_clash(self):
        self.actions.add("test_step", "1.step", 1)
        self.actions.add("test_result", "1.result", 1)
        assert len(self.actions) == 1
        with pytest.raises(pylatest.document.PylatestActionsError):
            self.actions.add("test_step", "1.step-clash", 1)
        assert len(self.actions) == 1
        assert list(self.actions.iter_content()) == ["1.step", "1.result"]
        assert list(self.actions) == [(1, '1.step', '1.result')]

    def test_actions_iter_twofull(self):
        self.actions.add("test_step", "1.step", 1)
        self.actions.add("test_result", "1.result", 1)
        self.actions.add("test_step", "2.step", 2)
        self.actions.add("test_result", "2.result", 2)
        assert list(self.actions) == \
               [(1, '1.step', '1.result'), (2, '2.step', '2.result')]

    def test_actions_add_auto_id(self):
        self.actions.add_step("1.step")
        assert list(self.actions) == [(1, '1.step', None)]
        self.actions.add_step("2.step")
        assert list(self.actions) == [
            (1, '1.step', None),
            (2, '2.step', None)]
        self.actions.add_result("3.result")
        assert list(self.actions) == [
            (1, '1.step', None),
            (2, '2.step', None),
            (3, None, '3.result')]

    def test_actions_add_auto_id_retval(self):
        auto_id = self.actions.add_step("step")
        assert auto_id == 1
        auto_id = self.actions.add_step("step")
        assert auto_id == 2
        auto_id = self.actions.add_result("result")
        assert auto_id == 3

    def test_actions_add_auto_id_reassign(self):
        new_id = self.actions.add_step("1.step", 1)
        assert new_id == 1
        assert list(self.actions) == [(1, '1.step', None)]

        second_id = pylatest.document.TestActions.MIN_AUTO_ID + 1
        new_id = self.actions.add_step("2.step", second_id)
        assert new_id == 2
        assert list(self.actions) == [
            (1, '1.step', None),
            (2, '2.step', None)]
        new_id = self.actions.add_result("2.result", second_id)
        assert new_id == 2
        assert list(self.actions) == [
            (1, '1.step', None),
            (2, '2.step', "2.result")]

        third_id = pylatest.document.TestActions.MIN_AUTO_ID + 123
        new_id = self.actions.add_step("3.step", third_id)
        assert new_id == 3
        assert list(self.actions) == [
            (1, '1.step', None),
            (2, '2.step', "2.result"),
            (3, '3.step', None)]


class TestSection(unittest.TestCase):

    def test_sections_eq(self):
        s1 = Section("Test Steps")
        s2 = Section("Test Steps")
        s3 = Section("Requirements")
        assert s1 == s2
        assert s2 != s3
        assert s1 != s3

    def test_plainhtml_id(self):
        s1 = Section("Description")
        assert s1.html_id == "description"

    def test_get_rst_header(self):
        s1 = Section("Test Case Description")
        exp_output = textwrap.dedent('''\
        Test Case Description
        =====================
        ''')
        assert s1.get_rst_header() == exp_output


class TestTestCaseDoc(unittest.TestCase):
    """
    Test properties of TestCaseDoc class.
    """

    def test_section_vs_sectionall_len(self):
        assert len(TestCaseDoc.SECTIONS) + 1 == len(TestCaseDoc.SECTIONS_ALL)

    def test_header_membership(self):
        assert TestCaseDoc._HEAD in TestCaseDoc.SECTIONS_ALL
        assert TestCaseDoc._HEAD not in TestCaseDoc.SECTIONS

    def test_sectionsall_contains_section(self):
        for section in TestCaseDoc.SECTIONS:
            assert section in TestCaseDoc.SECTIONS_ALL

    def test_has_section(self):
        assert TestCaseDoc.has_section(title="Description")
        assert TestCaseDoc.has_section("Test Steps")
        assert not TestCaseDoc.has_section(title="Requirements")
        assert not TestCaseDoc.has_section("Foo Bar")


class TestRstTestCaseDoc(unittest.TestCase):

    def test_rsttestcasedoc_empty(self):
        tc = RstTestCaseDoc()
        assert tc.is_empty()
        assert tc.sections == []
        assert tc.missing_sections == TestCaseDoc.SECTIONS_ALL

    def test_rsttestcasedoc_eq_self_empty(self):
        tc = RstTestCaseDoc()
        assert tc == tc

    def test_rsttestcasedoc_eq_empty(self):
        tc1 = RstTestCaseDoc()
        tc2 = RstTestCaseDoc()
        assert tc1 == tc2

    def test_rsttestcasedoc_add_section_simple(self):
        tc = RstTestCaseDoc()
        tc.add_section(TestCaseDoc.DESCR, "string content", lineno=42)
        assert not tc.is_empty()
        assert tc.sections == [TestCaseDoc.DESCR]
        assert sorted(tc.missing_sections + tc.sections) == \
               sorted(TestCaseDoc.SECTIONS_ALL)

    def test_rsttestcasedoc_add_section_multiple(self):
        tc = RstTestCaseDoc()
        tc.add_section(TestCaseDoc._HEAD, "header", lineno=42)
        tc.add_section(TestCaseDoc.DESCR, "description", lineno=83)
        assert not tc.is_empty()
        assert sorted(tc.sections) == \
               sorted([TestCaseDoc._HEAD, TestCaseDoc.DESCR])
        assert sorted(tc.missing_sections + tc.sections) == \
               sorted(TestCaseDoc.SECTIONS_ALL)

    def test_rsttestcasedoc_get_section_one(self):
        tc = RstTestCaseDoc()
        content = "some content of header section"
        tc.add_section(TestCaseDoc._HEAD, content, lineno=42)
        assert tc.get_section(TestCaseDoc._HEAD) == content

    def test_rsttestcasedoc_get_section_one_missing(self):
        tc = RstTestCaseDoc()
        tc.add_section(TestCaseDoc._HEAD, "some content", lineno=42)
        with pytest.raises(pylatest.document.PylatestDocumentError):
            tc.get_section(TestCaseDoc.DESCR)

    def test_rsttestcasedoc_add_section_multiple_duplicit(self):
        tc = RstTestCaseDoc()
        # set 1st value for DESCR section
        tc.add_section(TestCaseDoc.DESCR, "descr. one", lineno=42)
        # check that the 1st value has been included
        assert tc.get_section(TestCaseDoc.DESCR) == "descr. one"
        # 2nd value overrrides the original one
        tc.add_section(TestCaseDoc.DESCR, "descr. two", lineno=94)
        # check that the 2nd value has been included
        assert tc.get_section(TestCaseDoc.DESCR) == "descr. two"
        # additional checks
        assert not tc.is_empty()
        assert sorted(tc.sections) == sorted([TestCaseDoc.DESCR])
        assert sorted(tc.missing_sections + tc.sections) == \
               sorted(TestCaseDoc.SECTIONS_ALL)

    def test_rsttestcasedoc_add_section_few_multiple(self):
        tc = RstTestCaseDoc()
        tc.add_section(TestCaseDoc._HEAD, "header", lineno=10)
        tc.add_section(TestCaseDoc.DESCR, "description", lineno=55)
        tc.add_section(TestCaseDoc.SETUP, "setup", lineno=98)
        tc.add_section(TestCaseDoc.TEARD, "teardown", lineno=150)
        assert not tc.is_empty()
        assert sorted(tc.sections) == sorted([
            TestCaseDoc._HEAD,
            TestCaseDoc.DESCR,
            TestCaseDoc.SETUP,
            TestCaseDoc.TEARD])
        assert tc.missing_sections == [TestCaseDoc.STEPS]
        assert sorted(tc.missing_sections + tc.sections) == \
               sorted(TestCaseDoc.SECTIONS_ALL)

    def test_rsttestcasedoc_add_testaction_wrong(self):
        tc = RstTestCaseDoc()
        with pytest.raises(pylatest.document.PylatestActionsError):
            tc.add_test_action("test_foobarbaz", "content", 1)
        assert tc.is_empty()
        assert tc.sections == []
        assert tc.missing_sections == TestCaseDoc.SECTIONS_ALL
        assert sorted(tc.missing_sections + tc.sections) == \
               sorted(TestCaseDoc.SECTIONS_ALL)

    def test_rsttestcasedoc_add_testaction_simple(self):
        tc = RstTestCaseDoc()
        tc.add_test_action("test_step", "content", 1)
        assert not tc.is_empty()
        assert tc.sections == [TestCaseDoc.STEPS]
        assert sorted(tc.missing_sections + tc.sections) == \
               sorted(TestCaseDoc.SECTIONS_ALL)

    def test_rsttestcasedoc_add_testaction_multiple(self):
        tc = RstTestCaseDoc()
        tc.add_test_action("test_step", "test step", 1)
        tc.add_test_action("test_result", "test result", 1)
        tc.add_test_action("test_step", "another test step", 2)
        assert not tc.is_empty()
        assert tc.sections == [TestCaseDoc.STEPS]
        assert sorted(tc.missing_sections + tc.sections) == \
               sorted(TestCaseDoc.SECTIONS_ALL)

    def test_rsttestcasedoc_add_testaction_multiple_duplicit(self):
        tc = RstTestCaseDoc()
        tc.add_test_action("test_step", "test step", 1)
        with pytest.raises(pylatest.document.PylatestActionsError):
            tc.add_test_action("test_step", "another test step", 1)
        assert not tc.is_empty()
        assert tc.sections == [TestCaseDoc.STEPS]
        assert sorted(tc.missing_sections + tc.sections) == \
               sorted(TestCaseDoc.SECTIONS_ALL)

    def test_rsttestcasedoc_eq_self_nonempty(self):
        tc = RstTestCaseDoc()
        tc.add_section(TestCaseDoc._HEAD, "header", lineno=10)
        tc.add_section(TestCaseDoc.DESCR, "description", lineno=55)
        tc.add_test_action("test_step", "test step", 1)
        tc.add_test_action("test_result", "test result", 1)
        tc.add_test_action("test_step", "another test step", 2)
        assert tc == tc
        assert not tc.is_empty()

    def test_rsttestcasedoc_eq_nonempty(self):
        tc1 = RstTestCaseDoc()
        tc2 = RstTestCaseDoc()
        for tc in (tc1, tc2):
            tc.add_section(TestCaseDoc._HEAD, "header", lineno=10)
            tc.add_section(TestCaseDoc.DESCR, "description", lineno=55)
            tc.add_test_action("test_step", "test step", 1)
            tc.add_test_action("test_result", "test result", 1)
            tc.add_test_action("test_step", "another test step", 2)
        assert tc1 == tc2
        assert tc1.is_empty() == tc2.is_empty()


class TestRstTestCaseDocBuild(unittest.TestCase):

    def test_rsttestcasedoc_build_rst_empty(self):
        tc = RstTestCaseDoc()
        assert tc.build_rst() == ""

    def test_rsttestcasedoc_build_rst_onesection(self):
        tc = RstTestCaseDoc()
        content = textwrap.dedent('''\
        Description
        ===========

        This is just demonstration of usage of pylatest and
        expected structure of rst document.

        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec a diam
        lectus.  Sed sit amet ipsum mauris. Maecenas congue ligula ac quam
        viverra nec consectetur ante hendrerit. Donec et mollis dolor. Praesent
        et diam eget libero egestas mattis sit amet vitae augue.
        ''')
        tc.add_section(TestCaseDoc.DESCR, content, lineno=55)
        assert tc.build_rst() == content

    def test_rsttestcasedoc_build_rst_onesection_header(self):
        tc = RstTestCaseDoc()
        content = textwrap.dedent('''\
        Hello World Test Case
        *********************

        :author: foo@example.com
        :date: 2015-11-06
        :comment: Hello world.
        ''')
        tc.add_section(TestCaseDoc._HEAD, content, lineno=11)
        assert tc.build_rst() == content

    def test_rsttestcasedoc_build_rst_multiple_sections(self):
        tc = RstTestCaseDoc()
        description = textwrap.dedent('''\
        Description
        ===========

        There is no Description.
        ''')
        setup = textwrap.dedent('''\
        Setup
        =====

        Lorem ipsum dolor sit amet, consectetur adipiscing elit.
        ''')
        expected_rst = textwrap.dedent('''\
        Description
        ===========

        There is no Description.

        Setup
        =====

        Lorem ipsum dolor sit amet, consectetur adipiscing elit.
        ''')
        tc.add_section(TestCaseDoc.SETUP, setup)
        tc.add_section(TestCaseDoc.DESCR, description)
        assert tc.build_rst() == expected_rst

    def test_rsttestcasedoc_build_rst_single_action(self):
        tc = RstTestCaseDoc()
        step_1 = textwrap.dedent('''\
        .. test_step:: 1

            List files in the volume: ``ls -a /mnt/helloworld``
        ''')
        expected_rst = textwrap.dedent('''\
        Test Steps
        ==========

        .. test_step:: 1

            List files in the volume: ``ls -a /mnt/helloworld``
        ''')
        tc.add_test_action("test_step", step_1, 1)
        assert tc.build_rst() == expected_rst

    def test_rsttestcasedoc_build_rst_single_action_single_section(self):
        tc = RstTestCaseDoc()
        step_1 = textwrap.dedent('''\
        .. test_step:: 1

            List files in the volume: ``ls -a /mnt/helloworld``
        ''')
        description = textwrap.dedent('''\
        Description
        ===========

        There is no Description.
        ''')
        expected_rst = textwrap.dedent('''\
        Description
        ===========

        There is no Description.

        Test Steps
        ==========

        .. test_step:: 1

            List files in the volume: ``ls -a /mnt/helloworld``
        ''')
        tc.add_test_action("test_step", step_1, 1)
        tc.add_section(TestCaseDoc.DESCR, description)
        assert tc.build_rst() == expected_rst

    def test_rsttestcasedoc_build_rst_multiple_actions(self):
        tc = RstTestCaseDoc()
        step_1 = textwrap.dedent('''\
        .. test_step:: 1

            List files in the volume: ``ls -a /mnt/helloworld``
        ''')
        result_1 = textwrap.dedent('''\
        .. test_result:: 1

            There are no files, output should be empty.
        ''')
        step_2 = textwrap.dedent('''\
        .. test_step:: 2

            Donec et mollis dolor::

                $ foo --extra sth
                $ bar -vvv
        ''')
        expected_rst = textwrap.dedent('''\
        Test Steps
        ==========

        .. test_step:: 1

            List files in the volume: ``ls -a /mnt/helloworld``

        .. test_result:: 1

            There are no files, output should be empty.

        .. test_step:: 2

            Donec et mollis dolor::

                $ foo --extra sth
                $ bar -vvv
        ''')
        # call `add_test_action` in "random" order
        tc.add_test_action("test_step", step_2, 2)
        tc.add_test_action("test_result", result_1, 1)
        tc.add_test_action("test_step", step_1, 1)
        assert tc.build_rst() == expected_rst

    def test_rsttestcasedoc_build_rst_multiple_actions_autoid(self):
        tc = RstTestCaseDoc()
        step_1 = textwrap.dedent('''\
        .. test_step::

            List files in the volume: ``ls -a /mnt/helloworld``
        ''')
        result_1 = textwrap.dedent('''\
        .. test_result::

            There are no files, output should be empty.
        ''')
        step_2 = textwrap.dedent('''\
        .. test_step::

            Donec et mollis dolor::

                $ foo --extra sth
                $ bar -vvv
        ''')
        expected_rst = textwrap.dedent('''\
        Test Steps
        ==========

        .. test_step::

            List files in the volume: ``ls -a /mnt/helloworld``

        .. test_result::

            There are no files, output should be empty.

        .. test_step::

            Donec et mollis dolor::

                $ foo --extra sth
                $ bar -vvv
        ''')
        # don't include action ids
        tc.add_test_action("test_step", step_1, None)
        tc.add_test_action("test_result", result_1, None)
        tc.add_test_action("test_step", step_2, None)
        assert tc.build_rst() == expected_rst

    def test_rsttestcasedoc_build_rst_multiple_actions_with_section(self):
        """
        Note that when some test action directives are present, the actual
        content of test steps section is ignored (no matter what is there).
        """
        tc = RstTestCaseDoc()
        section_content = textwrap.dedent('''\
        Test Steps
        ==========

        .. test_step:: 1

            Here is the first step.

        .. test_result:: 1

            And the 2nd result.
        ''')
        step_2 = textwrap.dedent('''\
        .. test_step:: 2

            List files in the volume: ``ls -a /mnt/helloworld``
        ''')
        result_2 = textwrap.dedent('''\
        .. test_result:: 2

            There are no files, output should be empty.
        ''')
        step_3 = textwrap.dedent('''\
        .. test_step:: 3

            Donec et mollis dolor::

                $ foo --extra sth
                $ bar -vvv
        ''')
        expected_rst = textwrap.dedent('''\
        Test Steps
        ==========

        .. test_step:: 2

            List files in the volume: ``ls -a /mnt/helloworld``

        .. test_result:: 2

            There are no files, output should be empty.

        .. test_step:: 3

            Donec et mollis dolor::

                $ foo --extra sth
                $ bar -vvv
        ''')
        # call `add_test_action` in "random" order
        tc.add_test_action("test_step", step_3, 3)
        tc.add_test_action("test_result", result_2, 2)
        tc.add_test_action("test_step", step_2, 2)
        # and add test case section
        tc.add_section(TestCaseDoc.STEPS, section_content)
        assert tc.build_rst() == expected_rst


class TestXmlExportTestCaseDoc(unittest.TestCase):

    def test_xmltestcasedoc_sections(self):
        for section in XmlExportTestCaseDoc.SECTIONS:
            assert section.html_id is not None

    def test_xmltestcasedoc_empty(self):
        tc = XmlExportTestCaseDoc("Test Case Title Example")
        assert tc.is_empty()
        assert tc.sections == []
        # TODO: when missing_sections is implemented for xml export doc
        # assert tc.missing_sections == XmlExportTestCaseDoc.SECTIONS_ALL

    def test_xmltestcasedoc_eq_empty(self):
        tc1 = XmlExportTestCaseDoc(title="Example")
        tc2 = XmlExportTestCaseDoc(title="Example")
        assert tc1 == tc2

    def test_xmltestcasedoc_add_metadata(self):
        tc = XmlExportTestCaseDoc()
        assert tc.is_empty()
        assert len(tc.metadata) == 0
        tc.add_metadata("importance", "critical")
        assert not tc.is_empty()
        assert len(tc.metadata) == 1
        assert tc.metadata.get("importance") == "critical"

    def test_xmltestcasedoc_bad_contenttype(self):
        assert "foo" not in XmlExportTestCaseDoc.CONTENT_TYPES
        with pytest.raises(pylatest.document.PylatestDocumentError):
            tc = XmlExportTestCaseDoc(content_type="foo")


class TestXmlExportTestCaseDocBuild(unittest.TestCase):

    def test_xmltestcasedoc_build_xml_empty(self):
        tc = XmlExportTestCaseDoc()
        empty_xml = textwrap.dedent('''\
        <?xml version='1.0' encoding='utf-8'?>
        <testcase/>
        ''')
        assert tc.build_xml_string() == empty_xml

    def test_xmltestcasedoc_build_xml_empty_withid(self):
        tc = XmlExportTestCaseDoc(testcase_id="123")
        empty_xml = textwrap.dedent('''\
        <?xml version='1.0' encoding='utf-8'?>
        <testcase id="123"/>
        ''')
        assert tc.build_xml_string() == empty_xml

    def test_xmltestcasedoc_build_xml_title(self):
        tc = XmlExportTestCaseDoc(title="Foo Bar Test")
        exp_xml = textwrap.dedent('''\
        <?xml version='1.0' encoding='utf-8'?>
        <testcase>
          <title>Foo Bar Test</title>
        </testcase>
        ''')
        assert tc.build_xml_string() == exp_xml

    def test_xmltestcasedoc_build_xml_title_withid(self):
        tc = XmlExportTestCaseDoc(title="Foo Bar Test", testcase_id="113")
        exp_xml = textwrap.dedent('''\
        <?xml version='1.0' encoding='utf-8'?>
        <testcase id="113">
          <title>Foo Bar Test</title>
        </testcase>
        ''')
        assert tc.build_xml_string() == exp_xml

    def test_xmltestcasedoc_build_xml_meta(self):
        tc = XmlExportTestCaseDoc()
        tc.add_metadata("testtype", "functional")
        exp_xml = textwrap.dedent('''\
        <?xml version='1.0' encoding='utf-8'?>
        <testcase>
          <custom-fields>
            <custom-field content="functional" id="testtype"/>
          </custom-fields>
        </testcase>
        ''')
        assert tc.build_xml_string() == exp_xml

    # TODO: paramatrize
    def test_xmltestcasedoc_build_xml_setup(self):
        tc = XmlExportTestCaseDoc()
        tc.add_section(
            XmlExportTestCaseDoc.SETUP,
            etree.fromstring('<p xmlns="http://www.w3.org/1999/xhtml">This is setup.</p>'))
        exp_xml = textwrap.dedent('''\
        <?xml version='1.0' encoding='utf-8'?>
        <testcase>
          <custom-fields>
            <custom-field id="{}">
              <p xmlns="http://www.w3.org/1999/xhtml">This is setup.</p>
            </custom-field>
          </custom-fields>
        </testcase>
        ''').format(XmlExportTestCaseDoc.SETUP.html_id)
        assert tc.build_xml_string() == exp_xml

    def test_xmltestcasedoc_build_xml_setup_bad_contenttype(self):
        tc = XmlExportTestCaseDoc()
        tc.add_section(
            XmlExportTestCaseDoc.SETUP,
            etree.fromstring('<p xmlns="http://www.w3.org/1999/xhtml">This is setup.</p>'))
        assert "foo" not in XmlExportTestCaseDoc.CONTENT_TYPES
        tc.content_type = "foo"
        with pytest.raises(pylatest.document.PylatestDocumentError):
            tc.build_xml_string()

    def test_xmltestcasedoc_build_xml_setup_teardown(self):
        tc = XmlExportTestCaseDoc()
        tc.add_section(
            XmlExportTestCaseDoc.SETUP,
            etree.fromstring('<p xmlns="http://www.w3.org/1999/xhtml">This is setup.</p>'))
        tc.add_section(
            XmlExportTestCaseDoc.TEARD,
            etree.fromstring('<p xmlns="http://www.w3.org/1999/xhtml">This is teardown.</p>'))
        exp_xml = textwrap.dedent('''\
        <?xml version='1.0' encoding='utf-8'?>
        <testcase>
          <custom-fields>
            <custom-field id="{}">
              <p xmlns="http://www.w3.org/1999/xhtml">This is setup.</p>
            </custom-field>
            <custom-field id="{}">
              <p xmlns="http://www.w3.org/1999/xhtml">This is teardown.</p>
            </custom-field>
          </custom-fields>
        </testcase>
        ''').format(
            XmlExportTestCaseDoc.SETUP.html_id,
            XmlExportTestCaseDoc.TEARD.html_id)
        assert tc.build_xml_string() == exp_xml

    def test_xmltestcasedoc_build_xml_description(self):
        tc = XmlExportTestCaseDoc()
        tc.add_section(
            XmlExportTestCaseDoc.DESCR,
            etree.fromstring('<p xmlns="http://www.w3.org/1999/xhtml">This is a description</p>'))
        exp_xml = textwrap.dedent('''\
        <?xml version='1.0' encoding='utf-8'?>
        <testcase>
          <description>
            <p xmlns="http://www.w3.org/1999/xhtml">This is a description</p>
          </description>
        </testcase>
        ''')
        assert tc.build_xml_string() == exp_xml

    def test_xmltestcasedoc_build_xml_description_cdata(self):
        tc = XmlExportTestCaseDoc(content_type=XmlExportTestCaseDoc.CDATA)
        tc.add_section(
            XmlExportTestCaseDoc.DESCR,
            etree.fromstring('<p xmlns="http://www.w3.org/1999/xhtml">This is a description</p>'))
        exp_xml = textwrap.dedent('''\
        <?xml version='1.0' encoding='utf-8'?>
        <testcase>
          <description><![CDATA[<p>This is a description</p>]]></description>
        </testcase>
        ''')
        assert tc.build_xml_string() == exp_xml

    def test_xmltestcasedoc_build_xml_description_plaintext(self):
        tc = XmlExportTestCaseDoc(content_type=XmlExportTestCaseDoc.PLAINTEXT)
        tc.add_section(
            XmlExportTestCaseDoc.DESCR,
            etree.fromstring('<p xmlns="http://www.w3.org/1999/xhtml">This is a description</p>'))
        exp_xml = textwrap.dedent('''\
        <?xml version='1.0' encoding='utf-8'?>
        <testcase>
          <description>This is a description</description>
        </testcase>
        ''')
        assert tc.build_xml_string() == exp_xml

    def test_xmltestcasedoc_build_xml_action(self):
        tc = XmlExportTestCaseDoc()
        tc.add_test_action(
            "test_step",
            etree.fromstring('<p xmlns="http://www.w3.org/1999/xhtml">Step.</p>'),
            1)
        tc.add_test_action(
            "test_result",
            etree.fromstring('<p xmlns="http://www.w3.org/1999/xhtml">Nothing happens.</p>'),
            1)
        exp_xml = textwrap.dedent('''\
        <?xml version='1.0' encoding='utf-8'?>
        <testcase>
          <test-steps>
            <test-step>
              <test-step-column id="step">
                <p xmlns="http://www.w3.org/1999/xhtml">Step.</p>
              </test-step-column>
              <test-step-column id="expectedResult">
                <p xmlns="http://www.w3.org/1999/xhtml">Nothing happens.</p>
              </test-step-column>
            </test-step>
          </test-steps>
        </testcase>
        ''')
        assert tc.build_xml_string() == exp_xml

    def test_xmltestcasedoc_build_xml_action_cdata(self):
        tc = XmlExportTestCaseDoc(content_type=XmlExportTestCaseDoc.CDATA)
        tc.add_test_action(
            "test_step",
            etree.fromstring('<p xmlns="http://www.w3.org/1999/xhtml">Step.</p>'),
            1)
        tc.add_test_action(
            "test_result",
            etree.fromstring('<p xmlns="http://www.w3.org/1999/xhtml">Nothing happens.</p>'),
            1)
        exp_xml = textwrap.dedent('''\
        <?xml version='1.0' encoding='utf-8'?>
        <testcase>
          <test-steps>
            <test-step>
              <test-step-column id="step"><![CDATA[<p>Step.</p>]]></test-step-column>
              <test-step-column id="expectedResult"><![CDATA[<p>Nothing happens.</p>]]></test-step-column>
            </test-step>
          </test-steps>
        </testcase>
        ''')
        assert tc.build_xml_string() == exp_xml

    def test_xmltestcasedoc_build_xml_action_plaintext(self):
        tc = XmlExportTestCaseDoc(content_type=XmlExportTestCaseDoc.PLAINTEXT)
        tc.add_test_action(
            "test_step",
            etree.fromstring('<p xmlns="http://www.w3.org/1999/xhtml">Step.</p>'),
            1)
        tc.add_test_action(
            "test_result",
            etree.fromstring('<p xmlns="http://www.w3.org/1999/xhtml">Nothing happens.</p>'),
            1)
        exp_xml = textwrap.dedent('''\
        <?xml version='1.0' encoding='utf-8'?>
        <testcase>
          <test-steps>
            <test-step>
              <test-step-column id="step">Step.</test-step-column>
              <test-step-column id="expectedResult">Nothing happens.</test-step-column>
            </test-step>
          </test-steps>
        </testcase>
        ''')
        assert tc.build_xml_string() == exp_xml
