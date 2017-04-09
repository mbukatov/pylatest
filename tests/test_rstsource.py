# -*- coding: utf8 -*-

# Copyright (C) 2017 Martin Bukatovič <martin.bukatovic@gmail.com>
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


import os
import textwrap
import unittest

from pylatest.document import TestCaseDoc
import pylatest.rstsource as rstsource
import pylatest.xdocutils.core


class TestFindSections(unittest.TestCase):

    def setUp(self):
        # commons steps required for all test cases
        pylatest.xdocutils.core.register_all(use_plain=True)

    def test_find_sections_emptydoc(self):
        assert rstsource.find_sections("") == []

    def test_find_sections_doc_without_title(self):
        src = textwrap.dedent('''\
        There is no title or any sections. Just a paragraph.

        Or two.
        ''')
        assert rstsource.find_sections(src) == []

    def test_find_sections_docwithoutsections_one(self):
        src = textwrap.dedent('''\
        Hello World
        ***********

        There are no sections, just a document title.
        But in this case, it's evaluated as a section, so that
        we are able to detect section fragments.
        ''')
        exp_sections = [
            rstsource.RstSection("Hello World", 1, 6),
            ]
        assert rstsource.find_sections(src) == exp_sections

    def test_find_sections_docwithoutsections_one_another(self):
        """
        The same case as test_find_sections_docwithoutsections_one.
        """
        src = textwrap.dedent('''\
        Description
        ===========

        This is just demonstration of usage of pylatest rst directives and
        expected structure of rst document.

        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec a diam
        lectus.  Sed sit amet ipsum mauris. Maecenas congue ligula ac quam
        viverra nec consectetur ante hendrerit. Donec et mollis dolor. Praesent
        et diam eget libero egestas mattis sit amet vitae augue.

        See :RHBZ:`439858` for more details.
        ''')
        exp_sections = [
            rstsource.RstSection(TestCaseDoc.DESCR.title, 1, 12),
            ]
        assert rstsource.find_sections(src) == exp_sections

    def test_find_sections_docwithoutsections_two(self):
        src = textwrap.dedent('''\
        =============
         Hello World
        =============

        Again, there are no sections, just a document title.
        ''')
        assert rstsource.find_sections(src) == []

    def test_find_sections_metadata_doc_without_title(self):
        src = textwrap.dedent('''\
        There is no title or any sections. Just a paragraph and some metadata.

        :author: foo@example.com
        :date: 2015-11-06
        :comment: This is here just to test metadata processing.
        ''')
        assert rstsource.find_sections(src) == []

    def test_find_sections_metadata_simple_one(self):
        src = textwrap.dedent('''\
        Hello World Test Case
        *********************

        :author: foo@example.com
        :date: 2015-11-06
        :comment: This is here just to test metadata processing.


        ''')
        exp_sections = [
            rstsource.RstSection(None, 1, 8),
            ]
        assert rstsource.find_sections(src) == exp_sections

    def test_find_sections_metadata_simple_two(self):
        src = textwrap.dedent('''\
        Just Another Test Case
        **********************

        :author: foo.bar@example.com
        ''')
        exp_sections = [
            rstsource.RstSection(None, 1, 4),
            ]
        assert rstsource.find_sections(src) == exp_sections

    def test_find_sections_metadata_with_other_sections_one(self):
        src = textwrap.dedent('''\
        Just Another Test Case
        **********************

        :author: foo.bar@example.com

        Description
        ===========

        Vivamus fermentum semper porta. Nunc diam velit, adipiscing ut tristique
        vitae, sagittis vel odio. Maecenas convallis ullamcorper ultricies.
        ''')
        exp_sections = [
            rstsource.RstSection('Description', 6, 10),
            rstsource.RstSection(None, 1, 4),
            ]
        assert rstsource.find_sections(src) == exp_sections

    def test_find_sections_metadata_with_other_sections_two(self):
        src = textwrap.dedent('''\
        Hello World Test Case
        *********************

        :author: foo@example.com
        :date: 2015-11-06
        :comment: This is here just to test metadata processing.

        Section One
        ===========

        Foo.

        Section Two
        ===========

        Bar.
        ''')
        exp_sections = [
            rstsource.RstSection('Section One', 8, 11),
            rstsource.RstSection('Section Two', 13, 16),
            rstsource.RstSection(None, 1, 6),
            ]
        assert rstsource.find_sections(src) == exp_sections

    def test_find_sections_metadata_simple_wrong(self):
        src = textwrap.dedent('''\
        Hello World Test Case
        *********************

        :author: foo@example.com
        :date: 2015-11-06
        :comment: This is here just to test metadata processing.

        Section One
        ***********

        Foo.

        Section Two
        ***********

        Bar.
        ''')
        exp_sections = [
            rstsource.RstSection("Hello World Test Case", 1, 6),
            rstsource.RstSection('Section One', 8, 11),
            rstsource.RstSection('Section Two', 13, 16),
            ]
        assert rstsource.find_sections(src) == exp_sections

    def test_find_sections_simpledoc(self):
        src = textwrap.dedent('''\
        Section One
        ***********

        Foo.

        Section Two
        ***********

        Bar.
        ''')
        exp_sections = [
            rstsource.RstSection("Section One", 1, 4),
            rstsource.RstSection("Section Two", 6, 9),
            ]
        assert rstsource.find_sections(src) == exp_sections


    def test_find_sections_multilevel(self):
        src = textwrap.dedent('''\
        ===============
         Status Report
        ===============

        Lieber ein Spatz in der Hand als eine Taube auf dem Dach.

        Header One
        ==========

        Here is some text.

        .. while this line tries to hide itself

        Achtung
        ```````

        In this piece of code, we can see a similar issue::

           def foo(bar):
               return False

        Header Two
        ==========

        And here we have some text again.

        Header Three
        ============
        ''')
        exp_sections = [
            rstsource.RstSection("Header One", 7, 20),
            rstsource.RstSection("Header Two", 22, 25),
            rstsource.RstSection("Header Three", 27, 28),
            ]
        assert rstsource.find_sections(src) == exp_sections

    def test_find_sections_multilevel_with_testmetadata(self):
        src = textwrap.dedent('''\
        =============
         Test FooBar
        =============

        :author: foo@example.com
        :date: 2015-11-06

        Header One
        ==========

        Here is some text.

        .. while this line tries to hide itself

        Achtung
        ```````

        In this piece of code, we can see a similar issue::

           def foo(bar):
               return False

        Header Two
        ==========

        And here we have some text again.

        Header Three
        ============
        ''')
        exp_sections = [
            rstsource.RstSection("Header One", 8, 21),
            rstsource.RstSection("Header Two", 23, 26),
            rstsource.RstSection("Header Three", 28, 29),
            rstsource.RstSection(None, 1, 6),
            ]
        assert rstsource.find_sections(src) == exp_sections

    def test_find_sections_multilevel_startswithline(self):
        src = textwrap.dedent('''\
        Having some text like this before any title will make this rst
        document to lack a title.

        ===============
         Status Report
        ===============

        Lieber ein Spatz in der Hand als eine Taube auf dem Dach.

        Header One
        ==========

        Here is some text.

        .. while this line tries to hide itself

        Achtung
        ```````

        In this piece of code, we can see a similar issue::

           def foo(bar):
               return False

        Header Two
        ==========

        And here we have some text again.
        ''')
        exp_sections = [
            rstsource.RstSection("Status Report", 5, 28),
            ]
        assert rstsource.find_sections(src) == exp_sections


class TestGetLastLine(unittest.TestCase):

    def test_get_last_line_num_null(self):
        assert rstsource.get_last_line_num("") == 1

    def test_get_last_line_num_one(self):
        src = textwrap.dedent('''\
        1
        ''')
        assert rstsource.get_last_line_num(src) == 1

    def test_get_last_line_num_one_nonewline(self):
        src = "1"
        assert rstsource.get_last_line_num(src) == 1

    def test_get_last_line_num_four(self):
        src = textwrap.dedent('''\
        1
        2
        3
        4
        ''')
        assert rstsource.get_last_line_num(src) == 4

    def test_get_last_line_num_four_nonewline(self):
        src = textwrap.dedent('''\
        1
        2
        3
        4''')
        assert rstsource.get_last_line_num(src) == 4


class TestFindActions(unittest.TestCase):

    def setUp(self):
        # commons steps required for all test cases
        pylatest.xdocutils.core.register_all(use_plain=True)

    def test_find_actions_null(self):
        assert rstsource.find_actions("") == []

    def test_find_actions_emptydoc(self):
        src = textwrap.dedent('''\
        Test Steps
        ==========

        There are no rst directives.
        ''')
        assert rstsource.find_actions(src) == []

    def test_find_actions_somedoc_noaction(self):
        src = textwrap.dedent('''\
        =============
         Test FooBar
        =============

        :author: foo@example.com
        :date: 2015-11-06

        Header One
        ==========

        Here is some text.

        .. while this line tries to hide itself

        Achtung
        ```````

        In this piece of code, we can see a similar issue::

           def foo(bar):
               return False

        Test Steps
        ==========

        There are no rst directives in this section.
        ''')
        assert rstsource.find_actions(src) == []

    def test_find_actions_minimal_single_action(self):
        src = textwrap.dedent('''\
        .. test_step:: 1

            Maecenas congue ligula ac quam viverra nec
            consectetur ante hendrerit.

            This directive is the last node in this rst document.
        ''')
        exp_actions = [
            rstsource.RstTestAction(1, "test_step", 1, 6),
            ]
        assert rstsource.find_actions(src) == exp_actions

    def test_find_actions_minimal_single_action_highid(self):
        src = textwrap.dedent('''\
        .. test_step:: 3

            Maecenas congue ligula ac quam viverra nec
            consectetur ante hendrerit.

            This directive is the last node in this rst document.
        ''')
        exp_actions = [
            rstsource.RstTestAction(3, "test_step", 1, 6),
            ]
        assert rstsource.find_actions(src) == exp_actions

    def test_find_actions_minimal_two_actions(self):
        src = textwrap.dedent('''\
        .. test_step:: 1

            Maecenas congue ligula ac quam viverra nec
            consectetur ante hendrerit.

            This directive is the last node in this rst document.

        .. test_step:: 2

            Maecenas congue ligula ac quam viverra nec
            consectetur ante hendrerit.
        ''')
        exp_actions = [
            rstsource.RstTestAction(1, "test_step", 1, 6),
            rstsource.RstTestAction(2, "test_step", 8, 11),
            ]
        assert rstsource.find_actions(src) == exp_actions

    def test_find_actions_simpledoc_endline_theend(self):
        src = textwrap.dedent('''\
        Test Steps
        ==========

        .. test_step:: 10

            Maecenas congue ligula ac quam viverra nec
            consectetur ante hendrerit.

            This directive is the last node in this rst document.
        ''')
        exp_actions = [
            rstsource.RstTestAction(10, "test_step", 4, 9),
            ]
        assert rstsource.find_actions(src) == exp_actions

    def test_find_actions_simpledoc_endline_paragraph(self):
        src = textwrap.dedent('''\
        Test Steps
        ==========

        .. test_step:: 5

            Maecenas congue ligula ac quam viverra nec
            consectetur ante hendrerit.

            And that's all!

        There is some other text after the directive.
        ''')
        exp_actions = [
            rstsource.RstTestAction(5, "test_step", 4, 9),
            ]
        assert rstsource.find_actions(src) == exp_actions

    def test_find_actions_simpledoc_endline_section(self):
        src = textwrap.dedent('''\
        Test Steps
        ==========

        .. test_step:: 1

            Maecenas congue ligula ac quam viverra nec
            consectetur ante hendrerit.

            And that's all!

        New Section
        ===========

        There is new section after the directive.
        ''')
        exp_actions = [
            rstsource.RstTestAction(1, "test_step", 4, 9),
            ]
        assert rstsource.find_actions(src) == exp_actions

    def test_find_actions_simpledoc_endline_anotherdirective(self):
        src = textwrap.dedent('''\
        Test Steps
        ==========

        .. test_step:: 1

            Maecenas congue ligula ac quam viverra nec
            consectetur ante hendrerit.

            And that's all!

        .. test_step:: 2

            Maecenas congue ligula ac quam viverra nec
            consectetur ante hendrerit.
        ''')
        exp_actions = [
            rstsource.RstTestAction(1, "test_step", 4, 9),
            rstsource.RstTestAction(2, "test_step", 11, 14),
            ]
        assert rstsource.find_actions(src) == exp_actions

    def test_find_actions_somedoc_oneaction(self):
        src = textwrap.dedent('''\
        =============
         Test FooBar
        =============

        :author: foo@example.com
        :date: 2015-11-06

        Header One
        ==========

        Here is some text.

        .. while this line tries to hide itself

        Achtung
        ```````

        .. test_step:: 1

            Maecenas congue ligula ac quam viverra nec
            consectetur ante hendrerit.

        In this piece of code, we can see a similar issue::

           def foo(bar):
               return False

        Test Steps
        ==========

        There are no rst directives in this section.
        ''')
        exp_actions = [
            rstsource.RstTestAction(1, "test_step", 18, 21),
            ]
        assert rstsource.find_actions(src) == exp_actions

    # note: there is no way checking of mixed content like that would work
    # this is because of pylatest tranformations, which translates pending
    # nodes into particular action nodes
    # the only way to have this would include disabling transform phase during
    # rst parsing in pylatest.rstsource module
    def test_find_actions_mixed(self):
        src = textwrap.dedent('''\
        This looks little fishy.

        .. test_step:: 1

            list files in the volume: ``ls -a /mnt/helloworld``

        This just some line. Ignore it.

        .. test_result:: 1

            there are no files, output should be empty.

        And another one! Let's ignore it as well.

        .. test_step:: 2

            donec et mollis dolor::

                $ foo --extra sth
                $ bar -vvv

        Test Steps
        ==========

        This doesn't make any sense.

        .. test_result:: 2

            Maecenas congue ligula ac quam viverra nec
            consectetur ante hendrerit.

        Test Steps Subsection
        `````````````````````

        Yay!

        .. test_step:: 3

            This one has no matching test result.

        .. test_result:: 4

            And this result has no test step.

            Donec et mollis dolor::

                $ foo --extra sth
                $ bar -vvv

        Foo Bar Baz Section
        ===================

        Really, this looks weird. But find_sections() should work anyway.

        .. test_step:: 5

            List files in the volume: ``ls -a /mnt/helloworld``

            This is the last step.
        ''')
        exp_actions = [
            rstsource.RstTestAction(1, "test_step", 3, 5),
            rstsource.RstTestAction(1, "test_result", 9, 11),
            rstsource.RstTestAction(2, "test_step", 15, 20),
            rstsource.RstTestAction(2, "test_result", 27, 30),
            rstsource.RstTestAction(3, "test_step", 37, 39),
            rstsource.RstTestAction(4, "test_result", 41, 48),
            rstsource.RstTestAction(5, "test_step", 55, 59),
            ]
        assert rstsource.find_actions(src) == exp_actions

    def test_find_actions_real_looking_test_steps_section(self):
        src = textwrap.dedent('''\
        Test Steps
        ==========

        .. test_step:: 1

            list files in the volume: ``ls -a /mnt/helloworld``

        .. test_result:: 1

            there are no files, output should be empty.

        .. test_step:: 2

            donec et mollis dolor::

                $ foo --extra sth
                $ bar -vvv

        .. test_result:: 2

            Maecenas congue ligula ac quam viverra nec
            consectetur ante hendrerit.

        .. test_step:: 3

            This one has no matching test result.

        .. test_result:: 4

            And this result has no test step.

            Donec et mollis dolor::

                $ foo --extra sth
                $ bar -vvv

        .. test_step:: 5

            List files in the volume: ``ls -a /mnt/helloworld``

            This is the last step.
        ''')
        exp_actions = [
            rstsource.RstTestAction(1, "test_step", 4, 6),
            rstsource.RstTestAction(1, "test_result", 8, 10),
            rstsource.RstTestAction(2, "test_step", 12, 17),
            rstsource.RstTestAction(2, "test_result", 19, 22),
            rstsource.RstTestAction(3, "test_step", 24, 26),
            rstsource.RstTestAction(4, "test_result", 28, 35),
            rstsource.RstTestAction(5, "test_step", 37, 41),
            ]
        assert rstsource.find_actions(src) == exp_actions
