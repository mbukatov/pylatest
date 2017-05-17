# -*- coding: utf8 -*-

# Copyright (C) 2017 Martin Bukatovič <mbukatov@redhat.com>
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


from os import path
import codecs
import logging

from docutils.io import StringOutput
from docutils.frontend import OptionParser
from lxml import etree
from sphinx.builders import Builder
from sphinx.util.osutil import ensuredir, os_path
from sphinx.writers.html import HTMLWriter, HTMLTranslator
from sphinx.highlighting import PygmentsBridge

from pylatest.xdocutils.nodes import test_action_node
from pylatest.export import build_xml_testcase_doc, build_xml_export_doc


logger = logging.getLogger(__name__)


class XmlExportBuilder(Builder):
    """
    Builds XML export file with html content.

    The builder extends base Builder class with as minimal extra attributes as
    possible to use HTMLWriter (sphinx html writer). I originally wanted to
    extend StandaloneHTMLBuilder instead, but I would need to disable most of
    it's functionality anyway.
    """
    # the builder's name, for the -b command line option
    name = 'xmlexport'
    # the builder's output format, or '' if no document output is produced,
    # value used for self.tags (instance of sphinx.util.tags.Tags)
    format = 'html'
    # allow parallel write_doc() calls
    allow_parallel = False

    # from StandaloneHTMLBuilder, not directly mentioned in Builder
    out_suffix = '.xml'
    link_suffix = '.xml'
    supported_image_types = []
    add_permalinks = False

    def init(self):
        # writer object is initialized in prepare_writing method
        self.writer = None
        # section numbers for headings in the currently visited document
        self.secnumbers = {}
        # figure numbers
        self.fignumbers = {}
        # currently written docname
        self.current_docname = None  # type: unicode
        # docutils translator
        self.translator_class = HTMLTranslator
        # sphinx highlighter, from StandaloneHTMLBuilder.init_highlighter()
        self.highlighter = PygmentsBridge(
            'html',
            'sphinx',
            self.config.trim_doctest_flags)

    # TODO: proper implementation
    def get_target_uri(self, docname, typ=None):
        # type: (unicode, unicode) -> unicode
        """Return the target URI for a document name.

        *typ* can be used to qualify the link characteristic for individual
        builders.
        """
        return docname + self.link_suffix

    # TODO: proper implementation
    def get_outdated_docs(self):
        # type: () -> Iterator[unicode]
        """Return an iterable of output files that are outdated, or a string
        describing what an update build will build.

        If the builder does not output individual files corresponding to
        source files, return a string here.  If it does, return an iterable
        of those files that need to be written.
        """
        for docname in self.env.found_docs:
            yield docname

    def prepare_writing(self, docnames):
        # type: (Set[unicode]) -> None
        """A place where you can add logic before :meth:`write_doc` is run"""
        self.writer = HTMLWriter(self)
        self.settings = OptionParser(
            defaults=self.env.settings,
            components=(self.writer,),
            read_config_files=True).get_default_values()
        self.settings.compact_lists = bool(self.config.html_compact_lists)

    def write_doc(self, docname, doctree):
        # type: (unicode, nodes.Node) -> None
        """Where you actually write something to the filesystem."""

        # hack: check if the document is a test case
        is_testcase_doc = False
        for node in doctree.traverse(test_action_node):
            is_testcase_doc = True
            break
        # we will produce xml export output for test cases only
        if not is_testcase_doc:
            return

        # generate html output from the doctree
        destination = StringOutput(encoding='utf-8')  # TODO: what is this?
        doctree.settings = self.settings
        self.current_docname = docname
        self.writer.write(doctree, destination)

        # generate content of target xml file based on html output
        tc_doc = build_xml_testcase_doc(
            html_source=self.writer.output,
            mixedcontent=self.app.config.pylatest_export_mixedcontent,
            )

        # validate and drop invalid metadata if needed
        if len(self.app.config.pylatest_valid_export_metadata) > 0:
            for name in list(tc_doc.metadata.keys()):
                if name not in self.app.config.pylatest_valid_export_metadata:
                    del tc_doc.metadata[name]

        # create xml export document with single test case
        export_doc = build_xml_export_doc(
            project_id=self.app.config.pylatest_project_id,
            testcases=[tc_doc.build_element_tree()],
            )
        content_b = etree.tostring(
            export_doc,
            xml_declaration=True,
            encoding='utf-8',
            pretty_print=self.app.config.pylatest_export_pretty_print)
        content = content_b.decode('utf-8')

        # write content into file
        outfilename = path.join(
            self.outdir, os_path(docname) + self.out_suffix)
        ensuredir(path.dirname(outfilename))
        try:
            with codecs.open(outfilename, 'w', 'utf-8') as f:  # type: ignore
                f.write(content)
        except (IOError, OSError) as err:
            logger.warning("error writing file %s: %s", outfilename, err)

    def finish(self):
        # type: () -> None
        pass
