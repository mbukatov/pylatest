# -*- coding: utf-8 -*-

# Copyright (C) 2018 Martin Bukatovič <martin.bukatovic@gmail.com>
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


import io
import os

import lxml.html
import pytest

from testutil import xmlparse_testcase, get_metadata_from_build


@pytest.mark.parametrize("builder", [
    pytest.mark.sphinx('html', 'html', testroot='testdefaults-not-used'),
    pytest.mark.sphinx('xmlexport', 'xmlexport', testroot='testdefaults-not-used'),
    ])
def test_directive_not_used(app, status, warning, builder):
    """
    Check that build doesn't fail without the feature.
    """
    app.builder.build_all()


@pytest.mark.sphinx('html', testroot='testdefaults-flat')
def test_directive_html_content(app, status, warning):
    """
    Check that test_defaults directive doesn't produce any content.
    """
    app.builder.build_all()
    # get content of index.html file
    with io.open(os.path.join(app.outdir, 'index.html'), encoding='utf-8') as html_file:
        html_str = html_file.read()
    assert len(html_str) > 0
    # parse index.html and get div element with content
    html_tree = lxml.html.fromstring(html_str)
    div_tree_list = html_tree.xpath('//div[@class="body" and @role="main"]')
    assert len(div_tree_list) == 1
    div_tree = div_tree_list[0]
    # check that there is nothing in the content div
    div_b = lxml.html.tostring(div_tree, method="text", encoding="utf-8")
    div_str = div_b.decode('utf-8').strip()
    assert div_str == u"Test of pylatest_defaults¶"


@pytest.mark.parametrize("builder", [
    pytest.mark.sphinx('html', 'html', testroot='testdefaults-flat'),
    pytest.mark.sphinx('xmlexport', 'xmlexport', testroot='testdefaults-flat'),
    ])
def test_testcasemetadata_html_flat(app, status, warning, builder):
    app.builder.build_all()
    # parse test case document builds
    foo_tree = xmlparse_testcase(app.outdir, "test_foo", builder)
    bar_tree = xmlparse_testcase(app.outdir, "test_bar", builder)
    # get metadata
    foo_meta = get_metadata_from_build(foo_tree, builder)
    bar_meta = get_metadata_from_build(bar_tree, builder)
    # check metadata directly included in the files
    assert ('author', 'joe.foo@example.com') in foo_meta
    assert ('author', 'joe.bar@example.com') in bar_meta
    # check metadata added by test_defaults directive (in index.rst file)
    assert ('component', 'foobar') in foo_meta
    assert ('importance', 'high') in foo_meta
    assert ('component', 'foobar') in bar_meta
    assert ('importance', 'high') in bar_meta
    # there are no other metadata
    assert len(foo_meta) == 3
    assert len(bar_meta) == 3


@pytest.mark.parametrize("builder", [
    pytest.mark.sphinx('html', 'html', testroot='testdefaults-flat-override'),
    pytest.mark.sphinx('xmlexport', 'xmlexport', testroot='testdefaults-flat-override'),
    ])
def test_testcasemetadata_html_flat_override(app, status, warning, builder):
    """
    Check that values from test_defaults directive can override
    values specified directly in a test case.
    """
    app.builder.build_all()
    # get metadata
    foo_meta = get_metadata_from_build(
        xmlparse_testcase(app.outdir, "test_foo", builder),
        builder)
    bar_meta = get_metadata_from_build(
        xmlparse_testcase(app.outdir, "test_bar", builder),
        builder)
    # check metadata overriden by testdefaults directive,
    # in index.rst file, we set/override 'component' to value 'actium'
    for meta in foo_meta, bar_meta:
        comp_list = [val for (key, val) in meta if key == 'component']
        assert len(comp_list) == 1
        assert comp_list[0] == 'actium'


@pytest.mark.parametrize("builder", [
    pytest.mark.sphinx('html', 'html', testroot='testdefaults-nested'),
    pytest.mark.sphinx('xmlexport', 'xmlexport', testroot='testdefaults-nested'),
    ])
def test_testcasemetadata_html_nested(app, status, warning, builder):
    """
    Given 2 directories with test cases (foo and bar), check that
    all test cases inside has component metadata value set properly,
    as defined in index.rst file (via test_defaults directive).
    """
    app.builder.build_all()
    for tc_name in (
            "foo/test_one",
            "foo/test_two",
            "bar/test_ten",
            "bar/test_elewen"):
        meta = get_metadata_from_build(
            xmlparse_testcase(app.outdir, tc_name, builder),
            builder)
        component = tc_name.split("/")[0]
        assert ("component", component) in meta


@pytest.mark.parametrize("builder", [
    pytest.mark.sphinx('html', 'html', testroot='testdefaults-nested-multiple'),
    pytest.mark.sphinx('xmlexport', 'xmlexport', testroot='testdefaults-nested-multiple'),
    ])
def test_testcasemetadata_html_nested_multiple(app, status, warning, builder):
    app.builder.build_all()
    # get metadata
    one_meta = get_metadata_from_build(
        xmlparse_testcase(app.outdir, "foo/test_one", builder),
        builder)
    ten_meta = get_metadata_from_build(
        xmlparse_testcase(app.outdir, "foo/bar/test_ten", builder),
        builder)
    # check metadata defined in test_defaults of root index.rst file
    assert ('note', 'test') in one_meta
    assert ('note', 'test') in ten_meta
    # check metadata defined in test_defaults of foo/index.rst file
    assert ('component', 'foo') in one_meta
    assert ('component', 'foo') in ten_meta
    # check metadata defined in test_defaults of foo/bar/index.rst file
    assert ('subcomponent', 'bar') in ten_meta


@pytest.mark.parametrize("builder", [
    pytest.mark.sphinx('html', 'html', testroot='testdefaults-nested-multiple'),
    pytest.mark.sphinx('xmlexport', 'xmlexport', testroot='testdefaults-nested-multiple'),
    ])
def test_testcasemetadata_html_nested_multiple_override(app, status, warning, builder):
    app.builder.build_all()
    # get metadata
    two_meta = get_metadata_from_build(
        xmlparse_testcase(app.outdir, "foo/test_two", builder),
        builder)
    ten_meta = get_metadata_from_build(
        xmlparse_testcase(app.outdir, "foo/bar/test_ten", builder),
        builder)
    elewen_meta = get_metadata_from_build(
        xmlparse_testcase(app.outdir, "foo/bar/test_elewen", builder),
        builder)
    # check metadata defined both in test_defaults of root index.rst file and
    # the test case itself, default value should be used
    assert ('note', 'test') in two_meta
    # check metadata defined both in test_defaults of bar's index.rst file and
    # the test case itself, default value should be used
    assert ('subcomponent', 'bar') in elewen_meta
    # check metadata defined both in test_defaults of bar's and foo's index.rst
    # file default value from foo's index.rst file should be used
    assert ('type', 'functional') in ten_meta
    assert ('type', 'functional') in elewen_meta
