# -*- coding: utf8 -*-

"""
Tests of pylatest docutils extensions: pylatest.xdocutils module as a whole.

This means that tests in this module uses user level docutils API to build
rst source into html build and then checks the result.
"""

# Copyright (C) 2016 martin.bukatovic@gmail.com
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


import textwrap
import unittest

import pytest

import pylatest.xdocutils.client as xclient


class TestBasePlain(unittest.TestCase):
    """
    Tests to to make sure that docutils module isn't broken (via pylatest
    extensions) and still works fine.
    """

    def setUp(self):
        # register custom pylatest nodes with html translator
        xclient.register_plain()
        # show full diff (note: python3 unittest diff is much better)
        self.maxDiff = None

    def check_html_body(self, rst_input, exp_result):
        htmlbody_str = xclient.publish_parts_wrapper(rst_input)['html_body']
        assert htmlbody_str == exp_result


class TestDocutilsPlain(TestBasePlain):
    """
    Tests to to make sure that docutils module isn't broken (via pylatest
    extensions) and still works fine.
    """

    def test_doc_empty(self):
        rst_input = ""
        exp_result = textwrap.dedent('''\
        <div class="document">
        </div>
        ''')
        self.check_html_body(rst_input, exp_result)

    def test_doc_simple(self):
        rst_input = "Ceterum censeo Carthaginem esse delendam"
        exp_result = textwrap.dedent('''\
        <div class="document">
        <p>Ceterum censeo Carthaginem esse delendam</p>
        </div>
        ''')
        self.check_html_body(rst_input, exp_result)

    def test_doc_somedirective(self):
        rst_input = textwrap.dedent('''\
        .. container::

            Ceterum censeo Carthaginem esse delendam.
        ''')
        exp_result = textwrap.dedent('''\
        <div class="document">
        <div class="docutils container">
        Ceterum censeo Carthaginem esse delendam.</div>
        </div>
        ''')
        self.check_html_body(rst_input, exp_result)


class TestDocutilsTable(TestDocutilsPlain):
    """
    The same basic tests, but with pylatest table transformations.
    """

    def setUp(self):
        # register custom pylatest nodes with html translator
        xclient.register_table()
        # show full diff (note: python3 unittest diff is much better)
        self.maxDiff = None


class TestTestActionsPlain(TestBasePlain):
    """
    Test of test action directives and transformations.
    """

    def test_teststep_empty(self):
        rst_input = '.. test_step:: 1'
        exp_result = textwrap.dedent('''\
        <div class="document">
        <div action_id="1" action_name="step" class="pylatest_action">

        </div>
        </div>
        ''')
        self.check_html_body(rst_input, exp_result)

    def test_teststep_simple(self):
        rst_input = textwrap.dedent('''\
        .. test_step:: 1

            Ceterum censeo Carthaginem esse delendam.
        ''')
        exp_result = textwrap.dedent('''\
        <div class="document">
        <div action_id="1" action_name="step" class="pylatest_action">
        Ceterum censeo Carthaginem esse delendam.
        </div>
        </div>
        ''')
        self.check_html_body(rst_input, exp_result)

    def test_test_action_simple(self):
        rst_input = textwrap.dedent('''\
        .. test_step:: 1

            Ceterum censeo Carthaginem esse delendam.

        .. test_result:: 1

            This city is no more ... it has ceased to be ...
        ''')
        exp_result = textwrap.dedent('''\
        <div class="document">
        <div action_id="1" action_name="step" class="pylatest_action">
        Ceterum censeo Carthaginem esse delendam.
        </div>
        <div action_id="1" action_name="result" class="pylatest_action">
        This city is no more ... it has ceased to be ...
        </div>
        </div>
        ''')
        self.check_html_body(rst_input, exp_result)

    def test_test_actions_two(self):
        rst_input = textwrap.dedent('''\
        .. test_step:: 1

            Ceterum censeo Carthaginem esse delendam.

        .. test_result:: 1

            This city is no more ... it has ceased to be ...

        .. test_step:: 2

            Step foo.

        .. test_result:: 2

            Result bar.
        ''')
        exp_result = textwrap.dedent('''\
        <div class="document">
        <div action_id="1" action_name="step" class="pylatest_action">
        Ceterum censeo Carthaginem esse delendam.
        </div>
        <div action_id="1" action_name="result" class="pylatest_action">
        This city is no more ... it has ceased to be ...
        </div>
        <div action_id="2" action_name="step" class="pylatest_action">
        Step foo.
        </div>
        <div action_id="2" action_name="result" class="pylatest_action">
        Result bar.
        </div>
        </div>
        ''')
        self.check_html_body(rst_input, exp_result)


class TestTestActionsPlainAutoId(TestTestActionsPlain):
    """
    Test cases of autoid directive ... runs all test cases of superclass
    and some special cases when action id is ommited. Note that one can't
    ommit action id for 1st test step directive!
    """

    def setUp(self):
        # register custom pylatest nodes with html translator
        xclient.register_plain(auto_id=True)
        # show full diff (note: python3 unittest diff is much better)
        self.maxDiff = None

    @pytest.mark.xfail(reason="https://gitlab.com/mbukatov/pylatest/issues/11")
    def test_test_action_simple_autoid(self):
        rst_input = textwrap.dedent('''\
        .. test_step:: 1

            Ceterum censeo Carthaginem esse delendam.

        .. test_result::

            This city is no more ... it has ceased to be ...
        ''')
        exp_result = textwrap.dedent('''\
        <div class="document">
        <div action_id="1" action_name="step" class="pylatest_action">
        Ceterum censeo Carthaginem esse delendam.
        </div>
        <div action_id="1" action_name="result" class="pylatest_action">
        This city is no more ... it has ceased to be ...
        </div>
        </div>
        ''')
        self.check_html_body(rst_input, exp_result)

    @pytest.mark.xfail(reason="https://gitlab.com/mbukatov/pylatest/issues/11")
    def test_test_actions_two_autoid(self):
        rst_input = textwrap.dedent('''\
        .. test_step:: 1

            Ceterum censeo Carthaginem esse delendam.

        .. test_result::

            This city is no more ... it has ceased to be ...

        .. test_step::

            Step foo.

        .. test_result::

            Result bar.
        ''')
        exp_result = textwrap.dedent('''\
        <div class="document">
        <div action_id="1" action_name="step" class="pylatest_action">
        Ceterum censeo Carthaginem esse delendam.
        </div>
        <div action_id="1" action_name="result" class="pylatest_action">
        This city is no more ... it has ceased to be ...
        </div>
        <div action_id="2" action_name="step" class="pylatest_action">
        Step foo.
        </div>
        <div action_id="2" action_name="result" class="pylatest_action">
        Result bar.
        </div>
        </div>
        ''')
        self.check_html_body(rst_input, exp_result)


class TestTestActionsTable(TestBasePlain):
    """
    Test of test action directives and transformations.
    """

    def setUp(self):
        # register custom pylatest nodes with html translator
        xclient.register_table()
        # show full diff (note: python3 unittest diff is much better)
        self.maxDiff = None

    def test_teststep_empty(self):
        rst_input = '.. test_step:: 1'
        exp_result = textwrap.dedent('''\
        <div class="document">
        <table border="1" class="docutils">
        <colgroup>
        <col width="2%" />
        <col width="49%" />
        <col width="49%" />
        </colgroup>
        <thead valign="bottom">
        <tr><th class="head">&nbsp;</th>
        <th class="head">Step</th>
        <th class="head">Expected Result</th>
        </tr>
        </thead>
        <tbody valign="top">
        <tr><td>1</td>
        <td>&nbsp;</td>
        <td>&nbsp;</td>
        </tr>
        </tbody>
        </table>
        </div>
        ''')
        self.check_html_body(rst_input, exp_result)

    def test_teststep_simple(self):
        rst_input = textwrap.dedent('''\
        .. test_step:: 1

            Ceterum censeo Carthaginem esse delendam.
        ''')
        exp_result = textwrap.dedent('''\
        <div class="document">
        <table border="1" class="docutils">
        <colgroup>
        <col width="2%" />
        <col width="49%" />
        <col width="49%" />
        </colgroup>
        <thead valign="bottom">
        <tr><th class="head">&nbsp;</th>
        <th class="head">Step</th>
        <th class="head">Expected Result</th>
        </tr>
        </thead>
        <tbody valign="top">
        <tr><td>1</td>
        <td>Ceterum censeo Carthaginem esse delendam.</td>
        <td>&nbsp;</td>
        </tr>
        </tbody>
        </table>
        </div>
        ''')
        self.check_html_body(rst_input, exp_result)

    def test_test_action_simple(self):
        rst_input = textwrap.dedent('''\
        .. test_step:: 1

            Ceterum censeo Carthaginem esse delendam.

        .. test_result:: 1

            This city is no more ... it has ceased to be ...
        ''')
        exp_result = textwrap.dedent('''\
        <div class="document">
        <table border="1" class="docutils">
        <colgroup>
        <col width="2%" />
        <col width="49%" />
        <col width="49%" />
        </colgroup>
        <thead valign="bottom">
        <tr><th class="head">&nbsp;</th>
        <th class="head">Step</th>
        <th class="head">Expected Result</th>
        </tr>
        </thead>
        <tbody valign="top">
        <tr><td>1</td>
        <td>Ceterum censeo Carthaginem esse delendam.</td>
        <td>This city is no more ... it has ceased to be ...</td>
        </tr>
        </tbody>
        </table>
        </div>
        ''')
        self.check_html_body(rst_input, exp_result)

    def test_test_actions_two(self):
        rst_input = textwrap.dedent('''\
        .. test_step:: 1

            Ceterum censeo Carthaginem esse delendam.

        .. test_result:: 1

            This city is no more ... it has ceased to be ...

        .. test_step:: 2

            Step foo.

        .. test_result:: 2

            Result bar.
        ''')
        exp_result = textwrap.dedent('''\
        <div class="document">
        <table border="1" class="docutils">
        <colgroup>
        <col width="2%" />
        <col width="49%" />
        <col width="49%" />
        </colgroup>
        <thead valign="bottom">
        <tr><th class="head">&nbsp;</th>
        <th class="head">Step</th>
        <th class="head">Expected Result</th>
        </tr>
        </thead>
        <tbody valign="top">
        <tr><td>1</td>
        <td>Ceterum censeo Carthaginem esse delendam.</td>
        <td>This city is no more ... it has ceased to be ...</td>
        </tr>
        <tr><td>2</td>
        <td>Step foo.</td>
        <td>Result bar.</td>
        </tr>
        </tbody>
        </table>
        </div>
        ''')
        self.check_html_body(rst_input, exp_result)


class TestTestActionsTableAutoId(TestTestActionsTable):

    def setUp(self):
        # register custom pylatest nodes with html translator
        xclient.register_table(auto_id=True)
        # show full diff (note: python3 unittest diff is much better)
        self.maxDiff = None

    def test_test_action_simple_autoid(self):
        rst_input = textwrap.dedent('''\
        .. test_step:: 1

            Ceterum censeo Carthaginem esse delendam.

        .. test_result::

            This city is no more ... it has ceased to be ...
        ''')
        exp_result = textwrap.dedent('''\
        <div class="document">
        <table border="1" class="docutils">
        <colgroup>
        <col width="2%" />
        <col width="49%" />
        <col width="49%" />
        </colgroup>
        <thead valign="bottom">
        <tr><th class="head">&nbsp;</th>
        <th class="head">Step</th>
        <th class="head">Expected Result</th>
        </tr>
        </thead>
        <tbody valign="top">
        <tr><td>1</td>
        <td>Ceterum censeo Carthaginem esse delendam.</td>
        <td>This city is no more ... it has ceased to be ...</td>
        </tr>
        </tbody>
        </table>
        </div>
        ''')
        self.check_html_body(rst_input, exp_result)

    def test_test_actions_two_autoid(self):
        rst_input = textwrap.dedent('''\
        .. test_step:: 1

            Ceterum censeo Carthaginem esse delendam.

        .. test_result::

            This city is no more ... it has ceased to be ...

        .. test_step::

            Step foo.

        .. test_result::

            Result bar.
        ''')
        exp_result = textwrap.dedent('''\
        <div class="document">
        <table border="1" class="docutils">
        <colgroup>
        <col width="2%" />
        <col width="49%" />
        <col width="49%" />
        </colgroup>
        <thead valign="bottom">
        <tr><th class="head">&nbsp;</th>
        <th class="head">Step</th>
        <th class="head">Expected Result</th>
        </tr>
        </thead>
        <tbody valign="top">
        <tr><td>1</td>
        <td>Ceterum censeo Carthaginem esse delendam.</td>
        <td>This city is no more ... it has ceased to be ...</td>
        </tr>
        <tr><td>2</td>
        <td>Step foo.</td>
        <td>Result bar.</td>
        </tr>
        </tbody>
        </table>
        </div>
        ''')
        self.check_html_body(rst_input, exp_result)
