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

    Requirement field in a field list is identified by either "requirement" or
    "requirements" field name, and it's possible to have multiple requirement
    items in a field list::

        <field_list>
            <field>
                ...
            <field>
                <field_name>
                    requirements
                <field_body>
                    ...
            <field>
                <field_name>
                    requirement
                <field_body>
                    ...

    Few examples of expected doctree structure of a requirement's field body::

        <field_body>
            <paragraph>
                FOO-130

    Or::

        <field_body>
            <paragraph>
                <reference refuri="https://example.com">
                    https://example.com

    Or::

        <field_body>
            <bullet_list bullet="-">
                <list_item>
                    <paragraph>
                        FOO-132
    """
    requirement_field_names = ("requirement", "requirements")
    requirements = []
    field_list = get_field_list(doctree)
    if field_list is None:
        return requirements
    for field in field_list.traverse(docutils.nodes.field):
        field_name = field[0].astext()
        # check few asumptions about the field as a whole
        if field_name not in requirement_field_names:
            continue
        field_body = field[1]
        if len(field_body) < 1:
            continue
        # processing of the field body (by rst node type in field body)
        if field_body[0].tagname == "paragraph":
            # drop the paragraph node
            item = field_body[0][0]
            requirements.append(item)
        elif field_body[0].tagname == "bullet_list":
            for item in field_body[0]:
                # drop list item wrapper nodes <list_item: <paragraph...>>
                if item.tagname == "list_item":
                    if len(item) > 0:
                        item = item[0]
                    else:
                        # the list item is empty, skip the item
                        continue
                if item.tagname == "paragraph":
                    item = item[0]
                requirements.append(item)
    return requirements
