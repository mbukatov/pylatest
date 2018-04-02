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

from lxml import etree

from testutil import xmlparse_testcase


@pytest.fixture
def xml_schema():
    """
    Returns lxml object with XMLSchema of xml export document.
    """
    with open("tests/xsphinx/import-testcases.xsd", "r") as schema_file:
        schema_doc = etree.parse(schema_file)
        schema = etree.XMLSchema(schema_doc)
        yield schema


@pytest.mark.sphinx('xmlexport', testroot='export_schema_validation')
def test_xml_schema_validation(app, status, warning, xml_schema):
    app.builder.build_all()
    # parse test case document builds
    bar_tree = xmlparse_testcase(app.outdir, "test_bar", "xmlexport")
    baz_tree = xmlparse_testcase(app.outdir, "test_baz", "xmlexport")
    # validate the xml documents
    assert xml_schema.validate(bar_tree)
    assert xml_schema.validate(baz_tree)
