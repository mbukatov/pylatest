# -*- coding: utf8 -*-

"""
Pylatest test case document module.

This module contains information about expected structure of pylatest document
types (eg. list of section titles) and other general functions.
"""

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


from lxml import etree


class PylatestDocumentError(Exception):
    pass


class PylatestActionsError(PylatestDocumentError):
    pass


class TestActions(object):
    """
    List of test actions, content of *Test Steps* section of a test case
    document.

    Action is couple of a test step and result with the same *action id*.

    Example
    -------

    Here is the rst source text of some *test action* with *action id* 42::

        .. test_step:: 42

            some step here

        .. test_result:: 42

            some result here

    And the expected structure of actions dict (see self._actions_dict)::

        actions_dict = {42: {'test_step': node_a, 'test_result': node_b}}

    where node_a and node_b are pending nodes of the step and resul directives.
    """

    ACTION_NAMES = ('test_step', 'test_result')
    """
    List of valid names of all pylatest actions.

    note: htmlplain div element uses just 'step' and 'result' - TODO: refactor?
    """

    MIN_AUTO_ID = 1000000000
    """
    Minimal value of action id for which new id should be assigned.
    """

    # TODO: consider changing inner representation (replace action_dict with
    # something else).

    def __init__(self, enforce_id=True):
        self._actions_dict = {}
        self._enforce_id = enforce_id
        self._action_id_cache = {}

    def __len__(self):
        return len(self._actions_dict)

    def __eq__(self, other):
        return self._actions_dict == other._actions_dict

    def __repr__(self):
        return str(self._actions_dict)

    def __iter__(self):
        """
        Iterate over actions, yielding: *action id* and content of test step
        and test result (None is used if step or result is not specified).
        """
        for action_id, action_dict in sorted(self._actions_dict.items()):
            step = action_dict.get('test_step')
            result = action_dict.get('test_result')
            yield action_id, step, result

    def iter_action(self):
        """
        Iterate over all actions, but yield each test step or result as
        a single item in a tuple: action_id, action_name, content.
        """
        for action_id, action_dict in sorted(self._actions_dict.items()):
            for name in self.ACTION_NAMES:
                content = action_dict.get(name)
                if content is None:
                    continue
                yield action_id, name, content

    def iter_content(self):
        """
        Iterate over all content.
        """
        for _, _, content in self.iter_action():
            yield content

    def _get_id(self):
        if len(self._actions_dict) == 0:
            return 1
        last_id = max(self._actions_dict.keys())
        return last_id + 1

    def add(self, action_name, content, action_id=None):
        if action_name not in self.ACTION_NAMES:
            msg = "invalid action_name: {0}".format(action_name)
            raise PylatestActionsError(msg)
        if action_id is None:
            action_id = self._get_id()
        elif action_id > TestActions.MIN_AUTO_ID:
            if action_id in self._action_id_cache:
                action_id = self._action_id_cache.pop(action_id)
            else:
                action_id_auto = action_id
                action_id = self._get_id()
                self._action_id_cache[action_id_auto] = action_id
        if self._enforce_id:
            action_dict = self._actions_dict.get(action_id)
            if action_dict is not None \
                    and action_dict.get(action_name) is not None:
                msg = "id error: such action has been already added"
                raise PylatestActionsError(msg)
        self._actions_dict.setdefault(action_id, {})[action_name] = content
        return action_id

    def add_step(self, content, action_id=None):
        return self.add("test_step", content, action_id)

    def add_result(self, content, action_id=None):
        return self.add("test_result", content, action_id)


class Section(object):
    """
    A section in pylatest reStructuredText document.

    This class is concerned just with document structure.
    """

    def __init__(self, title, html_id=True):
        self.title = title
        if html_id:
            self.html_id = title.lower()
        else:
            self.html_id = None

    def __eq__(self, other):
        return self.title == other.title

    def __hash__(self):
        return hash(self.title)

    def __lt__(self, other):
        return self.title < other.title

    def __le__(self, other):
        return self.title <= other.title

    def __gt__(self, other):
        return self.title > other.title

    def __ge__(self, other):
        return self.title >= other.title

    def __str__(self):
        return "Section({0})".format(self.title)

    def __repr__(self):
        return str(self)

    def get_rst_header(self):
        """
        Generate rst header code for this section.
        """
        return str(self.title) + '\n' + ('=' * len(self.title)) + '\n'


class TestCaseDoc(object):
    """
    Pylatest test case document.

    This class is concerned just with document structure.
    """

    DESCR = Section("Description")
    SETUP = Section("Setup")
    STEPS = Section("Test Steps", html_id=False)
    TEARD = Section("Teardown")
    _HEAD = Section("__header__", html_id=False)
    """
    Header pseudo section. It's not a real section, but a placeholder for data
    which includes:

     * main headline with a name of the test case
     * pylatest metadata directives

    Since this data can't be placed into a dedicated section (for obvious
    reasons: it's a main headline and immediate content with metadata), this
    header placeholder is not direcly included in ``SECTIONS`` tuple.
    """

    SECTIONS = [DESCR, SETUP, STEPS, TEARD]
    """
    List of sections expected in pylatest document (order matters).
    """

    SECTIONS_ALL = [_HEAD] + SECTIONS
    """
    List of titles of all sections in pylatest document (order matters),
    including HEADER pseudo section.
    """

    @classmethod
    def has_section(cls, title):
        """
        Check if given title matches some section of pylatest test case
        document.
        """
        for section in cls.SECTIONS:
            if section.title == title:
                return True
        return False


class TestCaseDocWithContent(TestCaseDoc):
    """
    Base class of pylatest test case document with content.
    """

    def __init__(self):
        self._test_actions = TestActions()
        # dictionary: Section -> string with rst source of given section.
        self._section_dict = {}

    def __eq__(self, other):
        return (self._section_dict == other._section_dict and
                self._test_actions == other._test_actions)

    def add_section(self, section, content):
        """
        Add string fragment which contains given sections.
        """
        self._section_dict[section] = content

    def get_section(self, section):
        """
        Return content of given section.

        Raises PylatestDocumentError when such section doesn't exist.

        This method was added for to simplify unit testing. It's not
        necessary for actual functionality.
        """
        content = self._section_dict.get(section)
        if content is None:
            msg = "section '{}' is not included in this document"
            raise PylatestDocumentError(msg.format(section))
        return content

    def add_test_action(self, action_name, content, action_id):
        """
        Add docstring which contains some test step or result directives.
        """
        self._test_actions.add(action_name, content, action_id)

    def is_empty(self):
        """
        Return True if the document is empty.
        """
        return len(self._section_dict) == 0 and len(self._test_actions) == 0

    @property
    def sections(self):
        """
        Return list of non empty sections of this document.
        """
        # TODO: define a order of sections somehow?
        section_list = list(self._section_dict.keys())
        if len(self._test_actions) > 0:
            section_list.append(TestCaseDoc.STEPS)
        return section_list

    @property
    def missing_sections(self):
        """
        Return list missing sections of this document.
        """
        missing_list = []
        for section in TestCaseDoc.SECTIONS_ALL:
            if section in self._section_dict:
                continue
            if section == TestCaseDoc.STEPS and len(self._test_actions) > 0:
                # test steps may be in standalone directives
                continue
            missing_list.append(section)
        return missing_list


class RstTestCaseDoc(TestCaseDocWithContent):
    """
    Pylatest test case document in ReStructuredText format.

    This class handles content as well, not just a document structure.

    The content is stored in rst string fragmens which could contain either:

    * one (or more) sections (eg. Description, Setup, Test Steps, Teardown)
    * one (or more) pylatest actions (test_step or test_result directives)

    Those two fragment sets are then combined to produce the rst string version
    of the document.
    """

    def __init__(self):
        super(RstTestCaseDoc, self).__init__()
        # name of python source file from which this document was extracted
        # TODO: set a proper value (lineno values are specified wrt this file)
        self._source_file = None

    def add_section(self, section, content, lineno=None):
        """
        Add string fragment which contains given sections.
        """
        super(RstTestCaseDoc, self).add_section(section, content)
        # TODO: process lineno

    def add_test_action(self, action_name, content, action_id, lineno=None):
        """
        Add docstring which contains some test step or result directives.
        """
        super(RstTestCaseDoc, self).add_test_action(
            action_name, content, action_id)
        # TODO: process lineno

    def build_rst(self):
        """
        Generate rst document.
        """
        if self.is_empty():
            return ""
        result_list = []
        for section in TestCaseDoc.SECTIONS_ALL:
            content = self._section_dict.get(section)
            # section "Test steps" requires special care
            if section == TestCaseDoc.STEPS:
                # we regenerate Test Steps section based on just test
                # actions ignoring any already existing content of the section
                # (if exists).
                if len(self._test_actions) > 0:
                    result_list.append(section.get_rst_header())
                    # put together test steps
                    for content in self._test_actions.iter_content():
                        result_list.append(content)
                # only when there are no test actions, we use content of
                # the test step section as it is - unless there is no such
                # content obviously ...
                elif content is not None:
                    result_list.append(content)
            # while all other sections are included as they are
            elif content is not None:
                result_list.append(content)
        return "\n".join(result_list)


class XmlExportTestCaseDoc(TestCaseDocWithContent):
    """
    XML export document.
    """

    SECTIONS = [
        TestCaseDocWithContent.DESCR,
        TestCaseDocWithContent.SETUP,
        TestCaseDocWithContent.TEARD]
    """
    List of sections expected in pylatest xml export document.
    """

    MIXEDCONTENT = "mixedcontent"
    CDATA = "CDATA"
    PLAINTEXT = "plaintext"
    CONTENT_TYPES = (
        MIXEDCONTENT,
        CDATA,
        PLAINTEXT,
        )
    """
    List of supported ways to include content in xml export file.
    """

    def __init__(self, title=None, content_type=None, testcase_id=None):
        super(XmlExportTestCaseDoc, self).__init__()
        self.metadata = {}
        self.title = title
        self.id = testcase_id
        if content_type is None:
            # use mixed content as the default
            self.content_type = self.MIXEDCONTENT
        elif content_type in self.CONTENT_TYPES:
            self.content_type = content_type
        else:
            msg = "unknown content type '{}'".format(content_type)
            raise PylatestDocumentError(msg)

    def __eq__(self, other):
        # TODO: use testcase id here?
        return (super(XmlExportTestCaseDoc, self).__eq__(other) and
                self.metadata == other.metadata and
                self.title == other.title)

    def _set_content(self, xml_node, html_node):
        if self.content_type == self.MIXEDCONTENT:
            xml_node.append(html_node)
        elif self.content_type == self.CDATA:
            # HACK: drop all namespaces
            # based on https://stackoverflow.com/questions/30232031/
            query = "descendant-or-self::*[namespace-uri()!='']"
            for element in html_node.xpath(query):
                element.tag = etree.QName(element).localname
            etree.cleanup_namespaces(html_node)
            # convert xhtml tree into string (now without xhtml namespace)
            content_b = etree.tostring(
                html_node,
                xml_declaration=False,
                encoding='utf-8',
                pretty_print=False)
            content_str = content_b.decode('utf-8')
            # and finally include this html string as a CDATA section
            xml_node.text = etree.CDATA(content_str)
        elif self.content_type == self.PLAINTEXT:
            xml_node.text = etree.tostring(
                html_node, method="text").decode('utf-8')
        else:
            msg = "unknown content type '{}'".format(self.content_type)
            raise PylatestDocumentError(msg)

    def is_empty(self):
        """
        Return True if the document is empty.
        """
        return (super(XmlExportTestCaseDoc, self).is_empty() and
                len(self.metadata) == 0)

    def add_metadata(self, attr_name, content):
        """
        Add test case metadata entry into xml export document.
        """
        self.metadata[attr_name] = content

    def build_element_tree(self):
        """
        Generate element tree representation of xml document.
        """
        testcase = etree.Element('testcase')
        # set testcase id
        if self.id is not None:
            testcase.set("id", str(self.id))
        # set tile
        if self.title is not None:
            title = etree.SubElement(testcase, 'title')
            title.text = self.title
        # set description
        if self.DESCR in self.sections:
            description = etree.SubElement(testcase, 'description')
            html_content = self.get_section(self.DESCR)
            self._set_content(description, html_content)
        # set test actions
        if len(self._test_actions) > 0:
            actions = etree.SubElement(testcase, 'test-steps')
        for action_id, step_html, result_html in self._test_actions:
            action = etree.SubElement(actions, 'test-step')
            if step_html is not None:
                step = etree.SubElement(
                    action,
                    'test-step-column',
                    attrib={'id': 'step'})
                self._set_content(step, step_html)
            if result_html is not None:
                result = etree.SubElement(
                    action,
                    'test-step-column',
                    attrib={'id': 'expectedResult'})
                self._set_content(result, result_html)
        # custom-fields contain metadata and setup and teardown
        if (len(self.metadata) > 0 or
                self.SETUP in self.sections or
                self.TEARD in self.sections):
            custom_fields = etree.SubElement(testcase, 'custom-fields')
        # set metadata
        for attr_name, content in self.metadata.items():
            etree.SubElement(
                custom_fields,
                'custom-field',
                attrib={'id': attr_name, 'content': content})
        # set setup and teardown
        for section in (self.SETUP, self.TEARD):
            if section in self.sections:
                html_content = self.get_section(section)
                custom_field = etree.SubElement(
                    custom_fields,
                    'custom-field',
                    attrib={'id': section.html_id})
                self._set_content(custom_field, html_content)
        # TODO: implement linking
        # linked_wis = etree.SubElement(testcase, 'linked-work-items')
        return testcase

    def build_xml_string(self):
        """
        Generate a string representation of xml document.
        """
        xml_tree = self.build_element_tree()
        content_b = etree.tostring(
            xml_tree,
            xml_declaration=True,
            encoding='utf-8',
            pretty_print=True)
        return content_b.decode('utf-8')
