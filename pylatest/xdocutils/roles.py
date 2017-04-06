# -*- coding: utf8 -*-

"""
ReStructuredText roles module.

See: http://docutils.sourceforge.net/docs/howto/rst-roles.html
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


import os

from docutils import nodes
from docutils import utils
from docutils.parsers.rst import roles


def redhat_bugzilla_role(role, rawtext, text, lineno, inliner,
                         options={}, content=[]):
    """
    Implementation of Red Hat Bugzilla referencing role.

    Usage::

        See :RHBZ:`439858` for more information.
    """
    try:
        bznum = int(text)
        if bznum <= 0:
            raise ValueError
    except ValueError:
        msg = inliner.reporter.error(
            'RHBZ number must be a number greater than or equal to 1; '
            '"%s" is invalid.' % text, line=lineno)
        prb = inliner.problematic(rawtext, rawtext, msg)
        return [prb], [msg]
    # TODO: make base url configurable
    ref = "https://bugzilla.redhat.com/show_bug.cgi?id={0:d}".format(bznum)
    roles.set_classes(options)
    node = nodes.reference(
        rawtext, 'RHBZ ' + utils.unescape(text), refuri=ref, **options)
    return [node], []

def pylaref_html_role(role, rawtext, text, lineno, inliner,
                      options={}, content=[]):
    """
    Implementation of pylatest reference role for html output.

    Usage::

        See :pylaref:`foobar` for more information.

    Where ``foobar`` is a pylatest document id.
    """
    doc_id = text
    # make the target path relative
    comp_num = len(doc_id.split("/"))
    relpath_list = ['..' for _ in range(comp_num - 1)]
    relpath_list.append(doc_id)
    relative_path = "{0:s}.html".format(os.path.join(*relpath_list))
    # create result
    roles.set_classes(options)
    node = nodes.reference(
        rawtext, utils.unescape(text), refuri=relative_path, **options)
    return [node], []
