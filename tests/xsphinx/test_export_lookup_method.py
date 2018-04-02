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


import pytest

from testutil import xmlparse_testcase, get_metadata_from_build


# parametrization checks whether custom lookup method is used as a default when
# lookup method is not selected
@pytest.mark.parametrize("testroot", [
    pytest.mark.sphinx('xmlexport', 'custom', testroot='export_lookup_method-custom'),
    pytest.mark.sphinx('xmlexport', 'default', testroot='export_lookup_method-default'),
    ])
def test_lookup_method_custom_id_value(app, status, warning, testroot):
    app.builder.build_all()
    # parse test case document builds
    foo_tree = xmlparse_testcase(app.outdir, "test_foo", "xmlexport")
    bar_tree = xmlparse_testcase(app.outdir, "test_bar", "xmlexport")
    one_tree = xmlparse_testcase(app.outdir, "foo/bar/test_one", "xmlexport")
    two_tree = xmlparse_testcase(app.outdir, "foo/bar/test_two", "xmlexport")
    # check test case id values (generated based on doc name)
    assert foo_tree.xpath('/testcases/testcase/@id') == ["/test_foo"]
    assert bar_tree.xpath('/testcases/testcase/@id') == ["/test_bar"]
    assert one_tree.xpath('/testcases/testcase/@id') == ["/foo/bar/test_one"]
    assert two_tree.xpath('/testcases/testcase/@id') == ["/foo/bar/test_two"]


@pytest.mark.parametrize("testroot", [
    pytest.mark.sphinx('xmlexport', 'custom', testroot='export_lookup_method-custom'),
    pytest.mark.sphinx('xmlexport', 'default', testroot='export_lookup_method-default'),
    ])
def test_lookup_method_custom_properties(app, status, warning, testroot):
    app.builder.build_all()
    # parse test case document builds
    foo_tree = xmlparse_testcase(app.outdir, "test_foo", "xmlexport")
    bar_tree = xmlparse_testcase(app.outdir, "test_bar", "xmlexport")
    one_tree = xmlparse_testcase(app.outdir, "foo/bar/test_one", "xmlexport")
    two_tree = xmlparse_testcase(app.outdir, "foo/bar/test_two", "xmlexport")
    # check that properties are set as expected
    for tree in (foo_tree, bar_tree, one_tree, two_tree):
        val_xp = "/testcases/properties/property[@name='lookup-method']/@value"
        assert tree.xpath(val_xp) == ["custom"]


@pytest.mark.sphinx('xmlexport', testroot='export_lookup_method-id')
def test_lookup_method_id_id_value(app, status, warning):
    app.builder.build_all()
    # parse test case document builds
    one_tree = xmlparse_testcase(app.outdir, "test_0001", "xmlexport")
    two_tree = xmlparse_testcase(app.outdir, "test_0002", "xmlexport")
    # check test case id values (generated based on doc name)
    assert one_tree.xpath('/testcases/testcase/@id') == ["0001"]
    assert two_tree.xpath('/testcases/testcase/@id') == ["0002"]


@pytest.mark.sphinx('xmlexport', testroot='export_lookup_method-id')
def test_lookup_method_id_id_value_missing(app, status, warning):
    app.builder.build_all()
    # parse test case document builds
    none_tree = xmlparse_testcase(app.outdir, "test_none", "xmlexport")
    noid_tree = xmlparse_testcase(app.outdir, "test_noid", "xmlexport")
    # check test case id values (generated based on doc name)
    assert none_tree.xpath('/testcases/testcase/@id') == []
    assert noid_tree.xpath('/testcases/testcase/@id') == []


@pytest.mark.sphinx('xmlexport', testroot='export_lookup_method-id')
def test_lookup_method_id_properties(app, status, warning):
    app.builder.build_all()
    # parse test case document builds
    one_tree = xmlparse_testcase(app.outdir, "test_0001", "xmlexport")
    two_tree = xmlparse_testcase(app.outdir, "test_0002", "xmlexport")
    none_tree = xmlparse_testcase(app.outdir, "test_none", "xmlexport")
    noid_tree = xmlparse_testcase(app.outdir, "test_noid", "xmlexport")
    # check that properties are set as expected
    for tree in (one_tree, two_tree, noid_tree, none_tree):
        val_xp = "/testcases/properties/property[@name='lookup-method']/@value"
        assert tree.xpath(val_xp) == ["id"]


@pytest.mark.sphinx('xmlexport', testroot='export_lookup_method-id')
def test_lookup_method_id_removal_of_id_field(app, status, warning):
    app.builder.build_all()
    # parse test case document builds
    one_tree = xmlparse_testcase(app.outdir, "test_0001", "xmlexport")
    two_tree = xmlparse_testcase(app.outdir, "test_0002", "xmlexport")
    # check that there is no id in custom field list (test case metadata)
    for tree in (one_tree, two_tree):
        val_xp = "/testcases/testcase/custom-fields/custom-field[@id='id']"
        assert tree.xpath(val_xp) == []


@pytest.mark.sphinx('xmlexport', testroot='export_lookup_method-id_custom')
def test_lookup_method_id_custom_hybrid(app, status, warning):
    app.builder.build_all()
    # parse test case document builds
    one_tree = xmlparse_testcase(app.outdir, "test_0001", "xmlexport")
    noid_tree = xmlparse_testcase(app.outdir, "test_noid", "xmlexport")
    # check test case id values (generated based on doc name)
    assert one_tree.xpath('/testcases/testcase/@id') == ["0001"]
    assert noid_tree.xpath('/testcases/testcase/@id') == ["/test_noid"]
    # check that properties are set as expected
    val_xp = "/testcases/properties/property[@name='lookup-method']/@value"
    assert one_tree.xpath(val_xp) == ["id"]
    assert noid_tree.xpath(val_xp) == ["custom"]
