# -*- coding: utf8 -*-

"""
Miscellaneous ReStructuredText and Docutils utilities for pylatest.
"""

# Copyright (C) 2018 martin.bukatovic@gmail.com
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


import docutils.nodes


def get_field_list(doctree):
    """
    Find and get field list node in a doctree of a test case. Returns None
    when the field list is not found.

    Few assumptions about expected doctree structure::

        <document ...>
            <section>
                <title>
                    Title of the test case
                <field_list>
                    <field>
                        ...
                    <field>
                        ...
    Or::

        <document ...>
            <title>
                Title of the test case
            <field_list>
                <field>
                    ...
                <field>
                    ...
    """
    field_list = None
    if len(doctree) <= 0:
        return field_list
    if doctree[0].tagname == 'section':
        if len(doctree[0]) > 1 and doctree[0][1].tagname == 'field_list':
            field_list = doctree[0][1]
    else:
        if len(doctree) > 1 and doctree[1].tagname == 'field_list':
            field_list = doctree[1]
    return field_list


def get_testcase_id(doctree):
    """
    Get test case id from a field list in given doctree. If the id can't be
    found there, None is returned.

    When the id is found, the id field is removed from the field list.

    Few assumptions about expected doctree structure of a field list::

        <field_list>
            <field>
                ...
            <field>
                <field_name>
                    id
                <field_body>
                    <paragraph>
                        FOOBAR-007
    """
    testcase_id = None
    field_list = get_field_list(doctree)
    if field_list is None:
        return testcase_id
    for field in field_list.traverse(docutils.nodes.field):
        field_name = field[0].astext()
        if field_name == "id":
            testcase_id = field[1][0].astext()
            # remove id field entry from the field list
            field.parent.remove(field)
            break
    return testcase_id


def get_testcase_requirements(doctree):
    """
    Get requirement(s) of test case from a field list in given doctree.
    """
    requirements = []
    field_list = get_field_list(doctree)
    if field_list is None:
        return requirements
    for field in field_list.traverse(docutils.nodes.field):
        field_name = field[0].astext()
        if field_name == "requirement":
            requirements.append(field[1][0].astext())
        if field_name == "requirements":
            for item in field[1][0]:
                requirements.append(item.astext())
    return requirements
