# -*- coding: utf-8 -*-
"""
Sphinx test suite utilities, copied from ``tests/util.py`` file of Sphinx
project, commit 139e09d12023a255b206c1158487d215217be920.

Some code from ``run.py`` file has been included here so that the tests
are executable via plain pytest.

Done as a workaround for: https://github.com/sphinx-doc/sphinx/issues/3458
"""

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
#
# This file incorporates work covered by the following copyright and
# permission notice:
#
#    Copyright (c) 2007-2017 by the Sphinx team (see AUTHORS file).
#    All rights reserved.
#
#    Redistribution and use in source and binary forms, with or without
#    modification, are permitted provided that the following conditions are
#    met:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#
#    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#    A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#    OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#    SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#    LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#    DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#    THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#    (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#    OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


import os
import re
import sys
import warnings
from xml.etree import ElementTree

from six import string_types

import pytest

from docutils import nodes
from docutils.parsers.rst import directives, roles

from sphinx import application
from sphinx.builders.latex import LaTeXBuilder
from sphinx.ext.autodoc import AutoDirective
from sphinx.pycode import ModuleAnalyzer

from path import path


__all__ = [
    'rootdir', 'tempdir',
    'skip_unless_importable', 'Struct',
    'SphinxTestApp',
    'path',
    'remove_unicode_literals',
]


# code from run.py
testroot = os.path.dirname(__file__) or '.'
# find a temp dir for testing and clean it up now
os.environ['SPHINX_TEST_TEMPDIR'] = \
    os.path.abspath(os.path.join(testroot, 'build')) \
    if 'SPHINX_TEST_TEMPDIR' not in os.environ \
    else os.path.abspath(os.environ['SPHINX_TEST_TEMPDIR'])

rootdir = path(os.path.dirname(__file__) or '.').abspath()
tempdir = path(os.environ['SPHINX_TEST_TEMPDIR']).abspath()

# code from run.py
print('Temporary files will be placed in %s.' % tempdir)
if tempdir.exists():
    tempdir.rmtree()
tempdir.makedirs()


def assert_re_search(regex, text, flags=0):
    if not re.search(regex, text, flags):
        assert False, '%r did not match %r' % (regex, text)


def assert_not_re_search(regex, text, flags=0):
    if re.search(regex, text, flags):
        assert False, '%r did match %r' % (regex, text)


def assert_startswith(thing, prefix):
    if not thing.startswith(prefix):
        assert False, '%r does not start with %r' % (thing, prefix)


def assert_node(node, cls=None, xpath="", **kwargs):
    if cls:
        if isinstance(cls, list):
            assert_node(node, cls[0], xpath=xpath, **kwargs)
            if cls[1:]:
                if isinstance(cls[1], tuple):
                    assert_node(node, cls[1], xpath=xpath, **kwargs)
                else:
                    assert len(node) == 1, \
                        'The node%s has %d child nodes, not one' % (xpath, len(node))
                    assert_node(node[0], cls[1:], xpath=xpath + "[0]", **kwargs)
        elif isinstance(cls, tuple):
            assert len(node) == len(cls), \
                'The node%s has %d child nodes, not %r' % (xpath, len(node), len(cls))
            for i, nodecls in enumerate(cls):
                path = xpath + "[%d]" % i
                assert_node(node[i], nodecls, xpath=path, **kwargs)
        elif isinstance(cls, string_types):
            assert node == cls, 'The node %r is not %r: %r' % (xpath, cls, node)
        else:
            assert isinstance(node, cls), \
                'The node%s is not subclass of %r: %r' % (xpath, cls, node)

    for key, value in kwargs.items():
        assert key in node, 'The node%s does not have %r attribute: %r' % (xpath, key, node)
        assert node[key] == value, \
            'The node%s[%s] is not %r: %r' % (xpath, key, value, node[key])


def skip_unless_importable(module, msg=None):
    """Decorator to skip test if module is not importable."""
    try:
        __import__(module)
    except ImportError:
        return pytest.mark.skipif(True, reason=(msg or 'conditional skip'))
    else:
        return pytest.mark.skipif(False, reason=(msg or 'conditional skip'))


def etree_parse(path):
    with warnings.catch_warnings(record=False):
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        return ElementTree.parse(path)


class Struct(object):
    def __init__(self, **kwds):
        self.__dict__.update(kwds)


class SphinxTestApp(application.Sphinx):
    """
    A subclass of :class:`Sphinx` that runs on the test root, with some
    better default values for the initialization parameters.
    """

    def __init__(self, buildername='html', testroot=None, srcdir=None,
                 freshenv=False, confoverrides=None, status=None, warning=None,
                 tags=None, docutilsconf=None):
        if testroot is None:
            defaultsrcdir = 'root'
            testroot = rootdir / 'root'
        else:
            defaultsrcdir = 'test-' + testroot
            testroot = rootdir / 'roots' / ('test-' + testroot)
        if srcdir is None:
            srcdir = tempdir / defaultsrcdir
        else:
            srcdir = tempdir / srcdir

        if not srcdir.exists():
            testroot.copytree(srcdir)

        if docutilsconf is not None:
            (srcdir / 'docutils.conf').write_text(docutilsconf)

        builddir = srcdir / '_build'
#        if confdir is None:
        confdir = srcdir
#        if outdir is None:
        outdir = builddir.joinpath(buildername)
        if not outdir.isdir():
            outdir.makedirs()
#        if doctreedir is None:
        doctreedir = builddir.joinpath('doctrees')
        if not doctreedir.isdir():
            doctreedir.makedirs()
        if confoverrides is None:
            confoverrides = {}
#        if warningiserror is None:
        warningiserror = False

        self._saved_path = sys.path[:]
        self._saved_directives = directives._directives.copy()
        self._saved_roles = roles._roles.copy()

        self._saved_nodeclasses = set(v for v in dir(nodes.GenericNodeVisitor)
                                      if v.startswith('visit_'))

        try:
            application.Sphinx.__init__(self, srcdir, confdir, outdir, doctreedir,
                                        buildername, confoverrides, status, warning,
                                        freshenv, warningiserror, tags)
        except:
            self.cleanup()
            raise

    def cleanup(self, doctrees=False):
        AutoDirective._registry.clear()
        ModuleAnalyzer.cache.clear()
        LaTeXBuilder.usepackages = []
        sys.path[:] = self._saved_path
        sys.modules.pop('autodoc_fodder', None)
        directives._directives = self._saved_directives
        roles._roles = self._saved_roles
        for method in dir(nodes.GenericNodeVisitor):
            if method.startswith('visit_') and \
               method not in self._saved_nodeclasses:
                delattr(nodes.GenericNodeVisitor, 'visit_' + method[6:])
                delattr(nodes.GenericNodeVisitor, 'depart_' + method[6:])

    def __repr__(self):
        return '<%s buildername=%r>' % (self.__class__.__name__, self.builder.name)


_unicode_literals_re = re.compile(r'u(".*?")|u(\'.*?\')')


def remove_unicode_literals(s):
    return _unicode_literals_re.sub(lambda x: x.group(1) or x.group(2), s)


def find_files(root, suffix=None):
    for dirpath, dirs, files in os.walk(root, followlinks=True):
        dirpath = path(dirpath)
        for f in [f for f in files if not suffix or f.endswith(suffix)]:
            fpath = dirpath / f
            yield os.path.relpath(fpath, root)


def strip_escseq(text):
    return re.sub('\x1b.*?m', '', text)
