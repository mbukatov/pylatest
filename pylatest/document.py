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


from docutils.core import publish_doctree
from docutils import nodes

import pylatest.xdocutils.nodes


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

    # TODO: consider changing inner representation (replace action_dict with
    # something else).

    def __init__(self, enforce_id=True):
        self._actions_dict = {}
        self._enforce_id = enforce_id

    def __len__(self):
        return len(self._actions_dict)

    def __eq__(self, other):
        return self._actions_dict == other._actions_dict

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

    def _get_id(self, action_name):
        if len(self._actions_dict) == 0:
            return 1
        last_id = max(self._actions_dict.keys())
        if self._actions_dict[last_id].get(action_name) is None:
            return last_id
        else:
            return last_id + 1

    def add(self, action_name, content, action_id=None):
        if action_name not in self.ACTION_NAMES:
            msg = "invalid action_name: {0}".format(action_name)
            raise PylatestActionsError(msg)
        if action_id is None:
            action_id = self._get_id(action_name)
        if self._enforce_id:
            action_dict = self._actions_dict.get(action_id)
            if action_dict is not None \
                    and action_dict.get(action_name) is not None:
                msg = "id error: such action has been already added"
                raise PylatestActionsError(msg)
        self._actions_dict.setdefault(action_id, {})[action_name] = content

    def add_step(self, content, action_id=None):
        self.add("test_step", content, action_id)

    def add_result(self, content, action_id=None):
        self.add("test_result", content, action_id)


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
        return str(self.title) + '\n' + ('=' * len(self.title))


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

    # TODO: remove during further refactoring?
    SECTIONS_PLAINHTML = [s.html_id for s in SECTIONS if s.html_id is not None]
    """
    List of ids of expected sections in plainhtml export of pylatest document.
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
        tuple: list of detected sections (Section objects),
               number of test action directives
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
        section = Section(title=node.astext())
        if section in TestCaseDoc.SECTIONS:
            detected_sections.append(section)

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
        title_value = nodetree[title_index].astext()
        if title_index == 0 and not TestCaseDoc.has_section(title=title_value):
            detected_sections.insert(1, TestCaseDoc._HEAD)

    return detected_sections, test_directive_count


class RstTestCaseDoc(TestCaseDoc):
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
        self._docstrings = []
        """
        List of all docstrings with at least one section.
        """
        self._section_dict = {}
        """
        Index for the list of docstrings: section name -> list of docstrings.
        """
        self._test_actions = []
        """
        Dosctrings with test step/result directives only.
        """

    def add_section(self, docstring, lineno, sections):
        """
        Add string fragment which contains given sections.
        """
        self._docstrings.append(docstring)
        for section in sections:
            self._section_dict.setdefault(section, []).append(docstring)

    def add_test_action(self, docstring, lineno):
        """
        Add docstring which contains some test step or result directives.
        """
        self._test_actions.append(docstring)

    def is_empty(self):
        """
        Return True if the document is empty.
        """
        return len(self._docstrings) == 0 and len(self._test_actions) == 0

    # TODO: define a order of sections somehow?

    @property
    def sections(self):
        """
        Return list of non empty sections of this document.
        """
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
            if section not in self._section_dict:
                if section == TestCaseDoc.STEPS and len(self._test_actions) > 0:
                    # test steps may be in standalone directives
                    continue
                missing_list.append(section)
        return missing_list

    def check(self):
        """
        Perform sanity check of this document.
        """
        errors = []
        return errors

    # move out?
    def add_docstring(self, docstring, lineno):
        """
        Add docstring which contains given sections.
        """
        sections, test_directive_count = detect_docstring_sections(docstring)

        if len(sections) == 0 and test_directive_count == 0:
            status_success = False
        elif len(sections) == 0 and test_directive_count > 0:
            self.add_test_action(docstring, lineno)
            status_success = True
        elif len(sections) > 0 and test_directive_count == 0:
            if TestCaseDoc.STEPS in sections:
                # we have Test Steps section without test step directives
                msg = "found 'Test Steps' section without test step direcives"
                # self._add_error(msg, lineno)
            self.add_section(docstring, lineno, sections)
            status_success = True
        elif len(sections) > 0 and test_directive_count > 0:
            if TestCaseDoc.STEPS not in sections:
                msg = ("docstring with multiple sections contains test step"
                      " directives, but no 'Test Steps' section was found")
                # self._add_error(msg, lineno)
            self.add_section(docstring, lineno, sections)
            status_success = True

        return status_success

    def get_rst(self, ignore_errors=False):
        """
        Generate rst document.
        """
        if self.is_empty():
            return ""

        # when everything is just in a single string
        if len(self._docstrings) == 1:
            content_string = self._docstrings[0]
            return content_string + '\n'

        # document is splitted across multiple docstrings
        rst_list = []
        docstrings_used = set()
        for section in TestCaseDoc.SECTIONS_ALL:
            docstrings = self._section_dict.get(section)
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
