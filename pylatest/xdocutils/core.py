# -*- coding: utf8 -*-

"""
Pylatest docutils core module.

This module contains pylatest publisher convenience functions ``publish_*`` and
functions to register custom pylatest directives and roles.

Without these functions, docutils would not undersdand pylatest docutils
extensions (such as pylatest directives), eg. when you use ``rst2html`` from
docutils to process pylatest rst files, it would report warnings or even fail
on unknown rst directives, roles and so on.

See related docutils documentation:

 * https://docutils.readthedocs.io/en/sphinx-docs/peps/pep-0258.html#publisher
 * https://docutils.readthedocs.io/en/sphinx-docs/api/publisher.html
 * https://docutils.readthedocs.io/en/sphinx-docs/api/cmdline-tool.html
 * http://docutils.sourceforge.net/docs/howto/rst-directives.html
 * http://docutils.sourceforge.net/docs/howto/rst-roles.html
"""

# Copyright (C) 2015 Martin Bukatovič <mbukatov@redhat.com>
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


from docutils import core
from docutils import nodes
from docutils.parsers import rst
from docutils.writers.html4css1 import HTMLTranslator

from pylatest.xdocutils.directives import OldTestActionDirective
from pylatest.xdocutils.directives import TestActionDirective
from pylatest.xdocutils.readers import NoPlainReader, PlainReader
from pylatest.xdocutils.roles import redhat_bugzilla_role
import pylatest.xdocutils.htmltranslator
import pylatest.xdocutils.nodes


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
    Register (actually inject, this is kind of a hack) custom pylatest nodes
    into html4css1.HTMLTranslator. These custom nodes are used to wrap content
    of pylatest directives into div or span elements.
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
    rst.roles.register_local_role("rhbz", redhat_bugzilla_role)


def register_pylatest_directives():
    """
    Register custom pylatest directives.
    """
    rst.directives.register_directive("test_step", OldTestActionDirective)
    rst.directives.register_directive("test_result", OldTestActionDirective)
    rst.directives.register_directive("test_action", TestActionDirective)


def register_all(use_plain=False):
    """
    Register all custom pylatest items. Set use_plain to True for plain
    (machine readable) output.
    """
    register_pylatest_roles()
    register_pylatest_directives()
    if use_plain:
        register_pylatest_nodes()


def wrapper(kwargs, use_plain=False):
    if use_plain:
        kwargs["reader"] = PlainReader()
    else:
        kwargs["reader"] = NoPlainReader()
    kwargs["settings_overrides"] = HTML_OVERRIDES
    # let's not pullute kwargs passed into docutils publisher function
    if "use_plain" in kwargs:
        del kwargs["use_plain"]
    return kwargs


def pylatest_publish_cmdline(*args, **kwargs):
    """
    Pylatest publish_cmdline function.
    This is a wrapper of ``docutils.core.publish_cmdline()``.
    """
    use_plain = kwargs.get("use_plain", False)
    register_all(use_plain)
    kwargs = wrapper(kwargs, use_plain)
    return core.publish_cmdline(*args, **kwargs)


def pylatest_publish_parts(*args, **kwargs):
    """
    Pylatest publish parts function.
    This is a wrapper of ``docutils.core.publish_parts()``.
    """
    use_plain = kwargs.get("use_plain", False)
    register_all(use_plain)
    kwargs = wrapper(kwargs, use_plain)
    return core.publish_parts(*args, **kwargs)
