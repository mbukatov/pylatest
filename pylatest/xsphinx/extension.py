# -*- coding: utf8 -*-

# Copyright (C) 2017 Martin Bukatovič <martin.bukatovic@gmail.com>
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


import os.path

import docutils.nodes

from pylatest.xdocutils import directives
from pylatest.xdocutils import htmltranslator
from pylatest.xdocutils import nodes
from pylatest.xdocutils import roles
from pylatest.xdocutils import transforms
from pylatest.xsphinx import builders


# TODO: replace this hack with a proper solution (see dosctring for details)
def pylatest_transform_handler(app):
    """
    This handler fuction adds pylatest transforms based on value of
    app.builder.

    Note that this is ugly hack: these transforms are applied after Sphinx
    parses a reST document so that that they affect doctree cached in
    `_build/doctree` directory. Which is bad because cached doctree build
    should be the same no matter which builder is used.
    """
    if isinstance(app.builder, builders.XmlExportBuilder):
        # pylatest transforms for plain format
        app.add_transform(transforms.TestActionsPlainIdTransform)
    else:
        # pylatest transforms for human readable html output,
        # translates pylatest nodes into nice sections or tables
        app.add_transform(transforms.TestActionsTableTransform)
        app.add_transform(transforms.RequirementSectionTransform)


def pylatest_resolve_defaults(app, doctree, docname):
    """
    Propagate values from test_defautls directive into test cases.
    """
    # First, check if there are no test_defautls directives, it would mean no
    # values to push into test cases.
    env = app.builder.env
    if not hasattr(env, "pylatest_defaults"):
        return

    # Check few assumptions about expected doctree structure:
    #
    # <document ...>
    #     <section>
    #         <title>
    #             Title of the test case
    #         <field_list>
    #             <field>
    #                 <field_name>
    #                     author
    #                 <field_body>
    #                     <paragraph>
    #                         foo@example.com
    if doctree.tagname != 'document':
        return
    if len(doctree) == 0:
        return
    if doctree[0].tagname != 'section':
        return
    if len(doctree[0]) <= 1:
        return
    if doctree[0][0].tagname != 'title':
        return
    if doctree[0][1].tagname != 'field_list':
        return
    field_list = doctree[0][1]

    # get dir name part of current source rst file's docname
    dirname = os.path.dirname(docname)

    # check which defaults are applicable
    tmp_dir_names = []
    for name in env.pylatest_defaults.keys():
        if os.path.commonprefix([dirname, name]) == name:
            if name == '':
                level = 0
            else:
                level = len(list(name.split('/')))
            tmp_dir_names.append((level, name))
    # and sort dir names by level: defaults nested deep in the tree are used
    # first so that the top level defautls override the nested ones
    def_dir_names = [
        v for l, v in sorted(tmp_dir_names, key=lambda x: x[0], reverse=True)]

    # push default values (if any) into field_list
    for dir_name in def_dir_names:
        # get field list items, which are already directly present in test case
        field_list_tc = {}  # field_name string -> field_body node
        for field in field_list.traverse(docutils.nodes.field):
            name = field[0].astext()
            field_list_tc[name] = field[1]
        for name, body in env.pylatest_defaults[dir_name].items():
            # check if such field list entry is not already defined in the test
            # case document
            if name in field_list_tc:
                # override value of already defined field list item
                field_list_tc[name][0] = docutils.nodes.paragraph(text=body)
            else:
                # create new field entry structure
                field_name = docutils.nodes.field_name(text=name)
                field_body = docutils.nodes.field_body()
                field_body += docutils.nodes.paragraph(text=body)
                field = docutils.nodes.field()
                field += field_name
                field += field_body
                # append the entry into field list
                field_list += field


def setup(app):
    # pylatest roles
    app.add_role("rhbz", roles.redhat_bugzilla_role)

    # pylatest directives
    app.add_directive("test_step", directives.OldTestActionDirective)
    app.add_directive("test_result", directives.OldTestActionDirective)
    app.add_directive("test_action", directives.TestActionDirective)
    app.add_directive("requirement", directives.RequirementDirective)
    app.add_directive("test_defaults", directives.TestDefaultsDirective)

    # pylatest nodes (generated by directives above)
    for node_name in nodes.node_class_names:
        node_class = getattr(nodes, node_name)
        visit_func = getattr(htmltranslator, "visit_" + node_name)
        depart_func = getattr(htmltranslator, "depart_" + node_name)
        app.add_node(node_class, html=(visit_func, depart_func))

    # pylatest transforms are added based on app.builder value
    app.connect('builder-inited', pylatest_transform_handler)

    # propagate values from test_defautls directive
    app.connect('doctree-resolved', pylatest_resolve_defaults)

    # builder for xmlexport output
    app.add_builder(builders.XmlExportBuilder)

    # pylatest configuration
    app.add_config_value('pylatest_project_id', default=None, rebuild='html')
    app.add_config_value('pylatest_valid_export_metadata', [], 'env')
    app.add_config_value('pylatest_export_mixedcontent', True, 'html')
    app.add_config_value('pylatest_export_pretty_print', True, 'html')

    # sphinx plugin metadata
    return {'version': '0.1.0'}
