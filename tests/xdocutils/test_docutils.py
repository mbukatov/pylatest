# -*- coding: utf8 -*-

"""
Tests of pylatest docutils extensions: pylatest.xdocutils module as a whole,
which includes effects of pylatest transforms.

This means that tests in this module use user level docutils API to build
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

import pytest

from pylatest.xdocutils.core import pylatest_publish_parts


def _publish_html(rst_input, use_plain=True):
    parts = pylatest_publish_parts(
        rst_input, writer_name='html', use_plain=use_plain)
    return parts['html_body']


def test_docutilsworks_doc_empty():
    rst_input = ""
    exp_result = textwrap.dedent('''\
    <div class="document">
    </div>
    ''')
    assert _publish_html(rst_input, use_plain=True) == exp_result


def test_docutilsworks_doc_simple():
    rst_input = "Ceterum censeo Carthaginem esse delendam"
    exp_result = textwrap.dedent('''\
    <div class="document">
    <p>Ceterum censeo Carthaginem esse delendam</p>
    </div>
    ''')
    assert _publish_html(rst_input, use_plain=True) == exp_result


def test_docutilsworks_doc_somedirective():
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
    assert _publish_html(rst_input, use_plain=True) == exp_result


@pytest.fixture(
    scope="module",
    params=['.. test_step:: 1', '.. test_action::\n   :step:'])
def rst_input_teststep_empty(request):
    return request.param


def test_actions_plain_teststep_empty(rst_input_teststep_empty):
    exp_result = textwrap.dedent('''\
    <div class="document">
    <div action_id="1" action_name="test_step" class="pylatest_action">

    </div>
    </div>
    ''')
    assert _publish_html(rst_input_teststep_empty, use_plain=True) == exp_result


def test_actions_noplain_teststep_empty(rst_input_teststep_empty):
    exp_result = textwrap.dedent('''\
    <div class="document">
    <table border="1" class="docutils">
    <colgroup>
    <col width="6%" />
    <col width="47%" />
    <col width="47%" />
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
    assert _publish_html(rst_input_teststep_empty, use_plain=False) == exp_result


@pytest.fixture(
    scope="module",
    params=[
        textwrap.dedent('''\
        .. test_step:: 1

            Ceterum censeo Carthaginem esse delendam.
        '''),
        textwrap.dedent('''\
        .. test_action::
           :step:
               Ceterum censeo Carthaginem esse delendam.
        '''),
        ])
def rst_input_teststep_simple(request):
    return request.param


def test_actions_plain_teststep_simple(rst_input_teststep_simple):
    exp_result = textwrap.dedent('''\
    <div class="document">
    <div action_id="1" action_name="test_step" class="pylatest_action">
    Ceterum censeo Carthaginem esse delendam.
    </div>
    </div>
    ''')
    assert _publish_html(rst_input_teststep_simple, use_plain=True) == exp_result


def test_actions_noplain_teststep_simple(rst_input_teststep_simple):
    exp_result = textwrap.dedent('''\
    <div class="document">
    <table border="1" class="docutils">
    <colgroup>
    <col width="6%" />
    <col width="47%" />
    <col width="47%" />
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
    assert _publish_html(rst_input_teststep_simple, use_plain=False) == exp_result


@pytest.fixture(
    scope="module",
    params=[
        textwrap.dedent('''\
        .. test_step:: 1

            Ceterum censeo Carthaginem esse delendam.

        .. test_result:: 1

            This city is no more ... it has ceased to be ...
        '''),
        textwrap.dedent('''\
        .. test_action::
           :step: Ceterum censeo Carthaginem esse delendam.
           :result: This city is no more ... it has ceased to be ...
        '''),
        ])
def rst_input_test_action_simple(request):
    return request.param


def test_actions_plain_test_action_simple(rst_input_test_action_simple):
    exp_result = textwrap.dedent('''\
    <div class="document">
    <div action_id="1" action_name="test_step" class="pylatest_action">
    Ceterum censeo Carthaginem esse delendam.
    </div>
    <div action_id="1" action_name="test_result" class="pylatest_action">
    This city is no more ... it has ceased to be ...
    </div>
    </div>
    ''')
    assert _publish_html(rst_input_test_action_simple, use_plain=True) == exp_result


def test_actions_noplain_test_action_simple(rst_input_test_action_simple):
    exp_result = textwrap.dedent('''\
    <div class="document">
    <table border="1" class="docutils">
    <colgroup>
    <col width="6%" />
    <col width="47%" />
    <col width="47%" />
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
    assert _publish_html(rst_input_test_action_simple, use_plain=False) == exp_result


@pytest.fixture(
    scope="module",
    params=[
        textwrap.dedent('''\
        .. test_step:: 1

            Ceterum censeo Carthaginem esse delendam.

        .. test_result:: 1

            This city is no more ... it has ceased to be ...

        .. test_step:: 2

            Step foo.

        .. test_result:: 2

            Result bar.
        '''),
        textwrap.dedent('''\
        .. test_action::
           :step: Ceterum censeo Carthaginem esse delendam.
           :result: This city is no more ... it has ceased to be ...

        .. test_action::
           :step: Step foo.
           :result: Result bar.
        '''),
        ])
def rst_input_test_action_two(request):
    return request.param


def test_actions_plain_test_actions_two(rst_input_test_action_two):
    exp_result = textwrap.dedent('''\
    <div class="document">
    <div action_id="1" action_name="test_step" class="pylatest_action">
    Ceterum censeo Carthaginem esse delendam.
    </div>
    <div action_id="1" action_name="test_result" class="pylatest_action">
    This city is no more ... it has ceased to be ...
    </div>
    <div action_id="2" action_name="test_step" class="pylatest_action">
    Step foo.
    </div>
    <div action_id="2" action_name="test_result" class="pylatest_action">
    Result bar.
    </div>
    </div>
    ''')
    assert _publish_html(rst_input_test_action_two, use_plain=True) == exp_result


def test_actions_noplain_test_actions_two(rst_input_test_action_two):
    exp_result = textwrap.dedent('''\
    <div class="document">
    <table border="1" class="docutils">
    <colgroup>
    <col width="6%" />
    <col width="47%" />
    <col width="47%" />
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
    assert _publish_html(rst_input_test_action_two, use_plain=False) == exp_result


def test_actions_plain_autoid_test_action_simple_autoid():
    rst_input = textwrap.dedent('''\
    .. test_step:: 1

        Ceterum censeo Carthaginem esse delendam.

    .. test_action::
       :result: This city is no more ... it has ceased to be ...
    ''')
    exp_result = textwrap.dedent('''\
    <div class="document">
    <div action_id="1" action_name="test_step" class="pylatest_action">
    Ceterum censeo Carthaginem esse delendam.
    </div>
    <div action_id="2" action_name="test_result" class="pylatest_action">
    This city is no more ... it has ceased to be ...
    </div>
    </div>
    ''')
    assert _publish_html(rst_input, use_plain=True) == exp_result


def test_actions_plain_autoid_test_actions_two_autoid():
    rst_input = textwrap.dedent('''\
    .. test_step:: 1

        Ceterum censeo Carthaginem esse delendam.

    .. test_action::
       :result: This city is no more ... it has ceased to be ...

    .. test_action::
       :step: Step foo.
       :result: Result bar.
    ''')
    exp_result = textwrap.dedent('''\
    <div class="document">
    <div action_id="1" action_name="test_step" class="pylatest_action">
    Ceterum censeo Carthaginem esse delendam.
    </div>
    <div action_id="2" action_name="test_result" class="pylatest_action">
    This city is no more ... it has ceased to be ...
    </div>
    <div action_id="3" action_name="test_step" class="pylatest_action">
    Step foo.
    </div>
    <div action_id="3" action_name="test_result" class="pylatest_action">
    Result bar.
    </div>
    </div>
    ''')
    assert _publish_html(rst_input, use_plain=True) == exp_result


def test_actions_noplain_autoid_test_action_simple_autoid():
    rst_input = textwrap.dedent('''\
    .. test_step:: 1

        Ceterum censeo Carthaginem esse delendam.

    .. test_action::
       :result: This city is no more ... it has ceased to be ...
    ''')
    exp_result = textwrap.dedent('''\
    <div class="document">
    <table border="1" class="docutils">
    <colgroup>
    <col width="6%" />
    <col width="47%" />
    <col width="47%" />
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
    <tr><td>2</td>
    <td>&nbsp;</td>
    <td>This city is no more ... it has ceased to be ...</td>
    </tr>
    </tbody>
    </table>
    </div>
    ''')
    assert _publish_html(rst_input, use_plain=False) == exp_result


def test_actions_noplain_autoid_test_actions_two_autoid():
    rst_input = textwrap.dedent('''\
    .. test_step:: 1

        Ceterum censeo Carthaginem esse delendam.

    .. test_action::
       :result: This city is no more ... it has ceased to be ...

    .. test_action::
       :step: Step foo.
       :result: Result bar.
    ''')
    exp_result = textwrap.dedent('''\
    <div class="document">
    <table border="1" class="docutils">
    <colgroup>
    <col width="6%" />
    <col width="47%" />
    <col width="47%" />
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
    <tr><td>2</td>
    <td>&nbsp;</td>
    <td>This city is no more ... it has ceased to be ...</td>
    </tr>
    <tr><td>3</td>
    <td>Step foo.</td>
    <td>Result bar.</td>
    </tr>
    </tbody>
    </table>
    </div>
    ''')
    assert _publish_html(rst_input, use_plain=False) == exp_result


@pytest.fixture(
    scope="module",
    params=[
        textwrap.dedent('''\
        .. test_step:: 1

            List files in the volume: ``ls -a /mnt/helloworld``

        .. test_result:: 1

            There are no files, output should be empty.

        .. test_step:: 2

            Donec et mollis dolor::

                $ foo --extra sth
                $ bar -vvv

        .. test_result:: 2

            Maecenas congue ligula ac quam viverra nec
            consectetur ante hendrerit.

        .. test_step:: 3

            This one has no matching test result.

        .. test_result:: 4

            And this result has no test step.

        '''),
        textwrap.dedent('''\
        .. test_action::
           :step: List files in the volume: ``ls -a /mnt/helloworld``
           :result: There are no files, output should be empty.

        .. test_action::
           :step:
               Donec et mollis dolor::

                   $ foo --extra sth
                   $ bar -vvv

           :result:
               Maecenas congue ligula ac quam viverra nec
               consectetur ante hendrerit.

        .. test_action::
           :step: This one has no matching test result.

        .. test_action::
           :result: And this result has no test step.
        '''),
        ])
def rst_input_full_example(request):
    """
    Full example of pylatest action sections based on example test case
    document from contrib directory.
    """
    return request.param


def test_actions_noplain_full_example(rst_input_full_example):
    exp_result = textwrap.dedent('''\
    <div class="document">
    <table border="1" class="docutils">
    <colgroup>
    <col width="6%" />
    <col width="47%" />
    <col width="47%" />
    </colgroup>
    <thead valign="bottom">
    <tr><th class="head">&nbsp;</th>
    <th class="head">Step</th>
    <th class="head">Expected Result</th>
    </tr>
    </thead>
    <tbody valign="top">
    <tr><td>1</td>
    <td>List files in the volume: <tt class="docutils literal">ls <span class="pre">-a</span> /mnt/helloworld</tt></td>
    <td>There are no files, output should be empty.</td>
    </tr>
    <tr><td>2</td>
    <td><p class="first">Donec et mollis dolor:</p>
    <pre class="last literal-block">
    $ foo --extra sth
    $ bar -vvv
    </pre>
    </td>
    <td>Maecenas congue ligula ac quam viverra nec
    consectetur ante hendrerit.</td>
    </tr>
    <tr><td>3</td>
    <td>This one has no matching test result.</td>
    <td>&nbsp;</td>
    </tr>
    <tr><td>4</td>
    <td>&nbsp;</td>
    <td>And this result has no test step.</td>
    </tr>
    </tbody>
    </table>
    </div>
    ''')
    assert _publish_html(rst_input_full_example, use_plain=False) == exp_result


def test_actions_plain_full_example(rst_input_full_example):
    exp_result = textwrap.dedent('''\
    <div class="document">
    <div action_id="1" action_name="test_step" class="pylatest_action">
    List files in the volume: <tt class="docutils literal">ls <span class="pre">-a</span> /mnt/helloworld</tt>
    </div>
    <div action_id="1" action_name="test_result" class="pylatest_action">
    There are no files, output should be empty.
    </div>
    <div action_id="2" action_name="test_step" class="pylatest_action">
    <p>Donec et mollis dolor:</p>
    <pre class="literal-block">
    $ foo --extra sth
    $ bar -vvv
    </pre>

    </div>
    <div action_id="2" action_name="test_result" class="pylatest_action">
    Maecenas congue ligula ac quam viverra nec
    consectetur ante hendrerit.
    </div>
    <div action_id="3" action_name="test_step" class="pylatest_action">
    This one has no matching test result.
    </div>
    <div action_id="4" action_name="test_result" class="pylatest_action">
    And this result has no test step.
    </div>
    </div>
    ''')
    assert _publish_html(rst_input_full_example, use_plain=True) == exp_result
