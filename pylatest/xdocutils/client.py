# -*- coding: utf8 -*-

"""
Pylatest docutils client module.

Using this custom docutils client is necessary because we need to register
custom pylatest rst directives. Eg. if you use plain rst2html from docutils
to process pylatest rst files, it would report warnings about unknown
rst directives.

See related docutils docs:

 * http://docutils.sourceforge.net/docs/howto/rst-directives.html
 * http://docutils.sourceforge.net/docs/howto/rst-roles.html
"""

# Copyright (C) 2015 mbukatov@redhat.com
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


from docutils.parsers.rst import directives
from docutils.parsers.rst import roles
from docutils.core import publish_cmdline
from docutils.core import publish_parts
from docutils import nodes
from docutils.writers.html4css1 import HTMLTranslator

from pylatest.xdocutils.directives import TestActionTableDirective
from pylatest.xdocutils.directives import TestActionPlainDirective
from pylatest.xdocutils.directives import TestMetadataTableDirective
from pylatest.xdocutils.directives import TestMetadataPlainDirective
from pylatest.xdocutils.directives import RequirementPlainDirective
from pylatest.xdocutils.directives import RequirementSectionDirective
from pylatest.xdocutils.roles import redhat_bugzilla_role
from pylatest.xdocutils.roles import pylaref_html_role
import pylatest.xdocutils.nodes
import pylatest.xdocutils.htmltranslator


# override default settings of html writer
# see: http://docutils.sourceforge.net/docs/api/publisher.html
# see: http://docutils.sourceforge.net/docs/user/config.html
HTML_OVERRIDES = {
    # don't embed default stylesheet
    'embed_stylesheet': False,
    # don't use stylesheet at all
    'stylesheet_path': None,
    }

def register_pylatest_nodes():
    """
    Register custom pylatest nodes for test step and resutl sections.
    These custom nodes are used to wrap content of pylatest directives into div
    or span elements.
    """
    nodes._add_node_class_names(pylatest.xdocutils.nodes.node_class_names)
    for node_name in pylatest.xdocutils.nodes.node_class_names:
        visit_func_name = "visit_" + node_name
        depart_func_name = "depart_" + node_name
        setattr(HTMLTranslator, visit_func_name,
            getattr(pylatest.xdocutils.htmltranslator, visit_func_name))
        setattr(HTMLTranslator, depart_func_name,
            getattr(pylatest.xdocutils.htmltranslator, depart_func_name))

def register_pylatest_roles():
    """
    Register custom pylatest roles.
    """
    roles.register_local_role("bz", redhat_bugzilla_role)
    roles.register_local_role("pylaref", pylaref_html_role)

def register_table():
    """
    Register table generating implementation of pylatest rst directives
    and roles.
    """
    directives.register_directive("test_metadata", TestMetadataTableDirective)
    directives.register_directive("test_step", TestActionTableDirective)
    directives.register_directive("test_result", TestActionTableDirective)
    directives.register_directive("requirement", RequirementSectionDirective)
    register_pylatest_roles()

def register_plain():
    """
    Register plain implementation of pylatest rst directives and roles.
    This is intended for further processing (HTML only).
    """
    directives.register_directive("test_metadata", TestMetadataPlainDirective)
    directives.register_directive("test_step", TestActionPlainDirective)
    directives.register_directive("test_result", TestActionPlainDirective)
    directives.register_directive("requirement", RequirementPlainDirective)
    register_pylatest_roles()
    register_pylatest_nodes()

def publish_cmdline_html():
    """
    Main function for pylatest ``rst2html`` like command line client.

    See: ``bin/pylatest2html`` script for usage.
    """
    # see: http://docutils.sourceforge.net/docs/api/cmdline-tool.html
    publish_cmdline(writer_name='html', settings_overrides=HTML_OVERRIDES)

def publish_cmdline_pseudoxml():
    """
    Main function for pylatest ``rst2pseudoxml`` like command line client.

    See: ``bin/pylatest2pseudoxml`` script for usage.
    """
    publish_cmdline(writer_name='pseudoxml')

def publish_cmdline_man():
    """
    Main function for pylatest ``rst2html`` like command line client.

    See: ``bin/pylatest2man`` script for usage.
    """
    publish_cmdline(writer_name='manpage')

def publish_parts_wrapper(rst_document):
    """
    Publish method for pylatest.export module.
    """
    parts = publish_parts(
        source=rst_document,
        writer_name='html', settings_overrides=HTML_OVERRIDES)
    return parts
