# -*- coding: utf8 -*-

# Copyright (C) 2017,2018 Martin Bukatovič <martin.bukatovic@gmail.com>
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


def pylatest_transform_handler(app, doctree, docname):
    """
    This handler fuction adds pylatest transforms based on value of
    app.builder.
    """
    if isinstance(app.builder, builders.XmlExportBuilder):
        # pylatest transforms for plain format
        app.add_post_transform(transforms.TestActionsPlainIdTransform)
    else:
        # pylatest transforms for human readable html output,
        # translates pylatest nodes into nice sections or tables
        app.add_post_transform(transforms.TestActionsTableTransform)


def pylatest_requirements_transform_handler(app):
    """
    Add transform which builds reversed index for test case requirements
    in ``env.pylatest_requirements``.
    """
    app.add_transform(transforms.RequiremenIndexingTransform)


def pylatest_resolve_requirements(app, doctree, docname):
    """
    Generate list of requirements (for each ``requirementlist`` directive)
    based on reverse index of requirements as created by
    RequiremenIndexingTransform.
    """
    env = app.builder.env

    # check if there is no reversed index for requirements
    if not hasattr(env, "pylatest_requirements"):
        env.pylatest_requirements = {}

    for node in doctree.traverse(nodes.requirementlist_node):
        content_node = docutils.nodes.bullet_list()
        for req_node, cases in sorted(
                env.pylatest_requirements.values(),
                key=lambda item: item[0].astext()):
            req_item_node = docutils.nodes.list_item()
            req_item_para_node = docutils.nodes.paragraph()
            req_item_para_node += req_node
            req_item_node += req_item_para_node
            case_list_node = docutils.nodes.bullet_list()
            for case in sorted(cases):
                case_item_node = docutils.nodes.list_item()
                par_node = docutils.nodes.paragraph()
                # building reference to test case document manually, the link
                # text is absolute docname (instead of document title as used
                # in doc rst role)
                ref_node = docutils.nodes.reference('', "/" + case)
                ref_node['internal'] = True
                ref_node['refuri'] = app.builder.get_relative_uri(
                    docname, case)
                par_node += ref_node
                case_item_node += par_node
                case_list_node += case_item_node
            req_item_node += case_list_node
            content_node += req_item_node
        node.replace_self(content_node)


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
    app.add_directive("test_defaults", directives.TestDefaultsDirective)
    app.add_directive("requirementlist", directives.RequirementListDirective)

    # pylatest nodes (generated by directives above)
    for node_name in nodes.node_class_names:
        node_class = getattr(nodes, node_name)
        visit_func = getattr(htmltranslator, "visit_" + node_name)
        depart_func = getattr(htmltranslator, "depart_" + node_name)
        app.add_node(node_class, html=(visit_func, depart_func))

    # pylatest transforms are added based on app.builder value
    app.connect('doctree-resolved', pylatest_transform_handler)

    # propagate values from test_defautls directive
    app.connect('doctree-resolved', pylatest_resolve_defaults)

    # transforms and handlers related to requirements processing
    app.connect('builder-inited', pylatest_requirements_transform_handler)
    app.connect('doctree-resolved', pylatest_resolve_requirements)

    # builder for xmlexport output
    app.add_builder(builders.XmlExportBuilder)

    # pylatest configuration
    app.add_config_value('pylatest_project_id', default=None, rebuild='html')
    app.add_config_value('pylatest_valid_export_metadata', [], 'env')
    app.add_config_value('pylatest_export_content_type', None, 'html')
    app.add_config_value('pylatest_export_pretty_print', True, 'html')
    # TODO: see what to set for rebuild option
    app.add_config_value('pylatest_export_lookup_method', "custom", 'html')
    app.add_config_value('pylatest_export_dry_run', False, 'html')
    app.add_config_value('pylatest_export_response_properties', None, 'html')

    # pylatest css tweaks
    app.add_stylesheet('pylatest.css')
    # make sure the css file gets copied into _static dir during html build
    here = os.path.abspath(os.path.dirname(__file__))
    app.config.html_static_path.append(os.path.join(here, "pylatest.css"))

    # sphinx plugin metadata
    return {'version': '0.1.4'}
