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

from pylatest.export import get_metadata


def xmlparse_testcase(outdir, doc_name, builder):
    """
    Parse html testcase file via etree xml parser, so that
    functions from pylatest.export module can be used on the
    result.
    """
    builder2ext = {
        "html": ".html",
        "xmlexport": ".xml",
        }
    html_str = (outdir / (doc_name + builder2ext[builder])).text()
    if builder == "html":
        # remove html specific entities so that we can use xml parser
        html_str = html_str.replace('&nbsp;', '')
        html_str = html_str.replace('&copy;', '')
    # parse the source
    xml_tree = etree.fromstring(html_str.encode("utf8"))
    return xml_tree


def get_metadata_from_build(tree, builder):
    """
    Extracts test case metadata from given xmlexport tree.
    """
    metadata = []
    if builder == "html":
        metadata = get_metadata(tree)
    elif builder == "xmlexport":
        # asking for list of elements maching given xpath query
        el_list = tree.xpath('/testcases/testcase/custom-fields')
        # if there is no such element
        if len(el_list) == 0:
            return metadata
        for field in el_list[0]:
            id_value = field.get('id')
            content_value = field.get('content')
            metadata.append((id_value, content_value))
    return metadata
