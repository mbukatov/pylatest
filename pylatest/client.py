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

from pylatest.directives import TestStepsTableDirective
from pylatest.directives import TestStepsPlainDirective
from pylatest.directives import TestMetadataTableDirective
from pylatest.directives import TestMetadataPlainDirective
from pylatest.roles import redhat_bugzilla_role
from pylatest.roles import pylaref_html_role
import pylatest.nodes
import pylatest.htmltranslator


# override default settings of html writer
# see: http://docutils.sourceforge.net/docs/api/publisher.html
# see: http://docutils.sourceforge.net/docs/user/config.html
HTML_OVERRIDES = {
    # don't embed default stylesheet
    'embed_stylesheet': False,
    # don't use stylesheet at all
    'stylesheet_path': None,
    }

def register_table():
    """
    Register table generating implementation of pylatest rst directives
    and roles.
    """
    directives.register_directive("test_metadata", TestMetadataTableDirective)
    directives.register_directive("test_step", TestStepsTableDirective)
    directives.register_directive("test_result", TestStepsTableDirective)
    roles.register_local_role("bz", redhat_bugzilla_role)
    roles.register_local_role("pylaref", pylaref_html_role)


def register_plain():
    """
    Register plain implementation of pylatest rst directives and roles.
    This is intended for further processing (HTML only).
    """
    directives.register_directive("test_metadata", TestMetadataPlainDirective)
    directives.register_directive("test_step", TestStepsPlainDirective)
    directives.register_directive("test_result", TestStepsPlainDirective)
    roles.register_local_role("bz", redhat_bugzilla_role)
    roles.register_local_role("pylaref", pylaref_html_role)
    # custom nodes are used to wrap content of pylatest directives into div
    # or span elements
    nodes._add_node_class_names(pylatest.nodes.node_class_names)
    for node_name in pylatest.nodes.node_class_names:
        visit_func_name = "visit_" + node_name
        depart_func_name = "depart_" + node_name
        setattr(HTMLTranslator, visit_func_name,
            getattr(pylatest.htmltranslator, visit_func_name))
        setattr(HTMLTranslator, depart_func_name,
            getattr(pylatest.htmltranslator, depart_func_name))

def publish_cmdline_html():
    """
    Main function for pylatest ``rst2html`` like command line client.

    See: ``bin/pylatest2html`` script for usage.
    """
    # see: http://docutils.sourceforge.net/docs/api/cmdline-tool.html
    publish_cmdline(writer_name='html', settings_overrides=HTML_OVERRIDES)

def publish_parts_htmlbody(rst_document):
    """
    Publish method for pylatest.polarion module.

    Returns:
        string: html body of html rendering of given rst document
    """
    parts = publish_parts(
        source=rst_document,
        writer_name='html', settings_overrides=HTML_OVERRIDES)
    return parts['html_body']
