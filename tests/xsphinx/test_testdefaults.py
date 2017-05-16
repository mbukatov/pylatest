# -*- coding: utf-8 -*-

from lxml import etree
import lxml.html
import pytest

from pylatest.export import NS, get_metadata


def xmlparse_html_testcase(outdir, filename):
    """
    Parse html testcase file via etree xml parser, so that
    functions from pylatest.export module can be used on the
    result.
    """
    html_str = (outdir / filename).text()
    # remove html specific entities so that we can use xml parser
    html_str = html_str.replace('&nbsp;', '')
    html_str = html_str.replace('&copy;', '')
    # parse the source
    xml_tree = etree.fromstring(html_str.encode("utf8"))
    return xml_tree


@pytest.mark.sphinx('html', testroot='testdefaults-not-used')
def test_directive_not_used(app, status, warning):
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
    html_str = (app.outdir / 'index.html').text()
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


@pytest.mark.sphinx('html', testroot='testdefaults-flat')
def test_testcasemetadata_html_flat(app, status, warning):
    app.builder.build_all()
    # parse test case document html builds
    foo_html_tree = xmlparse_html_testcase(app.outdir, "test_foo.html")
    bar_html_tree = xmlparse_html_testcase(app.outdir, "test_bar.html")
    # get metadata
    foo_meta = get_metadata(foo_html_tree)
    bar_meta = get_metadata(bar_html_tree)
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


@pytest.mark.sphinx('html', testroot='testdefaults-flat-override')
def test_testcasemetadata_html_flat_override(app, status, warning):
    """
    Check that values from test_defaults directive can override
    values specified directly in a test case.
    """
    app.builder.build_all()
    # get metadata
    foo_meta = get_metadata(xmlparse_html_testcase(app.outdir, "test_foo.html"))
    bar_meta = get_metadata(xmlparse_html_testcase(app.outdir, "test_bar.html"))
    # check metadata overriden by testdefaults directive,
    # in index.rst file, we set/override 'component' to value 'actium'
    for meta in foo_meta, bar_meta:
        comp_list = [val for (key, val) in meta if key == 'component']
        assert len(comp_list) == 1
        assert comp_list[0] == 'actium'


@pytest.mark.sphinx('html', testroot='testdefaults-nested')
def test_testcasemetadata_html_nested(app, status, warning):
    """
    Given 2 directories with test cases (foo and bar), check that
    all test cases inside has component metadata value set properly,
    as defined in index.rst file (via test_defaults directive).
    """
    app.builder.build_all()
    for tc_name in (
            "foo/test_one.html",
            "foo/test_two.html",
            "bar/test_ten.html",
            "bar/test_elewen.html"):
        meta = get_metadata(xmlparse_html_testcase(app.outdir, tc_name))
        component = tc_name.split("/")[0]
        assert ("component", component) in meta


@pytest.mark.sphinx('html', testroot='testdefaults-nested-multiple')
def test_testcasemetadata_html_nested_multiple(app, status, warning):
    app.builder.build_all()
    # get metadata
    one_meta = get_metadata(xmlparse_html_testcase(app.outdir, "foo/test_one.html"))
    ten_meta = get_metadata(xmlparse_html_testcase(app.outdir, "foo/bar/test_ten.html"))
    # check metadata defined in test_defaults of root index.rst file
    assert ('note', 'test') in one_meta
    assert ('note', 'test') in ten_meta
    # check metadata defined in test_defaults of foo/index.rst file
    assert ('component', 'foo') in one_meta
    assert ('component', 'foo') in ten_meta
    # check metadata defined in test_defaults of foo/bar/index.rst file
    assert ('subcomponent', 'bar') in ten_meta


@pytest.mark.sphinx('html', testroot='testdefaults-nested-multiple')
def test_testcasemetadata_html_nested_multiple_override(app, status, warning):
    app.builder.build_all()
    # get metadata
    two_meta = get_metadata(xmlparse_html_testcase(
        app.outdir, "foo/test_two.html"))
    ten_meta = get_metadata(xmlparse_html_testcase(
        app.outdir, "foo/bar/test_ten.html"))
    elewen_meta = get_metadata(xmlparse_html_testcase(
        app.outdir, "foo/bar/test_elewen.html"))
    # check metadata defined both in test_defaults of root index.rst file and
    # the test case itself, default value should be used
    assert ('note', 'test') in two_meta
    # check metadata defined both in test_defaults of bar's index.rst file and
    # the test case itself, default value should be used
    assert ('subcomponent', 'bar') in elewen_meta
    # check metadata defined both in test_defaults of bar's and foo's index.rst file
    # default value from foo's index.rst file should be used
    assert ('type', 'functional') in ten_meta
    assert ('type', 'functional') in elewen_meta
