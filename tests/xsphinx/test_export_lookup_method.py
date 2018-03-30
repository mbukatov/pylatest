# -*- coding: utf-8 -*-

import pytest

from testutil import xmlparse_testcase, get_metadata_from_build


@pytest.mark.sphinx('xmlexport', testroot='export_lookup_method-custom')
def test_lookup_method_custom_id_value(app, status, warning):
    app.builder.build_all()
    # parse test case document builds
    foo_tree = xmlparse_testcase(app.outdir, "test_foo", "xmlexport")
    bar_tree = xmlparse_testcase(app.outdir, "test_bar", "xmlexport")
    # check test case id values (generated based on doc name)
    assert foo_tree.xpath('/testcases/testcase/@id') == ["/test_foo"]
    assert bar_tree.xpath('/testcases/testcase/@id') == ["/test_bar"]


@pytest.mark.sphinx('xmlexport', testroot='export_lookup_method-custom')
def test_lookup_method_custom_properties(app, status, warning):
    app.builder.build_all()
    # parse test case document builds
    foo_tree = xmlparse_testcase(app.outdir, "test_foo", "xmlexport")
    bar_tree = xmlparse_testcase(app.outdir, "test_bar", "xmlexport")
    # check that properties are set as expected
    assert foo_tree.xpath("/testcases/properties/property[@name='lookup-method']/@value") == ["custom"]
    assert bar_tree.xpath("/testcases/properties/property[@name='lookup-method']/@value") == ["custom"]
