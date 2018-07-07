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


from lxml import etree
import pytest


from testutil import xmlparse_testcase


# xml namespaces
NS = {'html': 'http://www.w3.org/1999/xhtml'}


@pytest.mark.parametrize("builder", [
    pytest.mark.sphinx('html', 'html', testroot='requirementlist-nested'),
    pytest.mark.sphinx('xmlexport', 'xmlexport', testroot='requirementlist-nested'),
    ])
def test_requirementlist_minimal(app, status, warning, builder):
    """
    Just checking that this doesn't fail.
    """
    app.builder.build_all()


@pytest.mark.sphinx('html', testroot='requirementlist-nested')
def test_requirementlist_present_nested_html(app, status, warning):
    app.builder.build_all()
    # parse requirements overview document
    doc_tree = xmlparse_testcase(app.outdir, "requirements", "html")
    # find and check the requirement list
    req_list = doc_tree.xpath(
        '//html:div[@id="requirements"]/html:ul/html:li',
        namespaces=NS)
    assert len(req_list) == 4
    # check that the list contains all requirements
    req_items = [i.text for i in req_list]
    assert "FOO-ALL" in req_items
    assert "FOO-111" in req_items
    assert "FOO-112" in req_items
    assert "FOO-212" in req_items
