# -*- coding: utf-8 -*-

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
