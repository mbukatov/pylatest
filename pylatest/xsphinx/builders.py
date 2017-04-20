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


from os import path
import codecs
import logging
import textwrap

from docutils.io import StringOutput
from docutils.frontend import OptionParser
from sphinx.builders import Builder
from sphinx.util.osutil import ensuredir, os_path
from sphinx.writers.html import HTMLWriter, HTMLTranslator
from sphinx.highlighting import PygmentsBridge

from pylatest.xdocutils.nodes import test_action_node


logger = logging.getLogger(__name__)


class XmlExportBuilder(Builder):
    """
    Builds XML export format.
    """
    # The builder's name, for the -b command line option.
    name = 'xmlexport'
    # The builder's output format, or '' if no document output is produced.
    # Used for self.tags only (instance of sphinx.util.tags.Tags)
    format = 'xmlexport'
    # Allow parallel write_doc() calls.
    allow_parallel = False

    # from StandaloneHTMLBuilder, not directly mentioned in Builder
    out_suffix = '.xml'
    link_suffix = '.xml'  # defaults to matching out_suffix
    supported_image_types = []
    add_permalinks = False

    def init(self):
        # writer object is initialized in prepare_writing method
        self.writer = None
        # section numbers for headings in the currently visited document
        self.secnumbers = {}  # type: Dict[unicode, Tuple[int, ...]]
        # figure numbers
        self.fignumbers = {}
        # currently written docname
        self.current_docname = None  # type: unicode
        self.translator_class = HTMLTranslator
        self.init_highlighter()

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

    # from StandaloneHTMLBuilder
    def init_highlighter(self):
        # type: () -> None
        # determine Pygments style and create the highlighter
        if self.config.pygments_style is not None:
            style = self.config.pygments_style
        elif self.theme:
            style = self.theme.get_confstr('theme', 'pygments_style', 'none')
        else:
            style = 'sphinx'
        self.highlighter = PygmentsBridge('html', style,
                                          self.config.trim_doctest_flags)

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

        # TODO: produce actual content
        template = textwrap.dedent('''\
        <?xml version="1.0" encoding="utf-8" ?>
        <xmlexport>
        <!-- content of {0} test case -->
        {1}
        </xmlexport>
        ''')
        destination = StringOutput(encoding='utf-8')  # TODO: what is this?
        doctree.settings = self.settings
        self.current_docname = docname
        self.writer.write(doctree, destination)
        output = template.format(docname, self.writer.output)

        # write content into file
        outfilename = path.join(self.outdir, os_path(docname) + self.out_suffix)
        ensuredir(path.dirname(outfilename))
        try:
            with codecs.open(outfilename, 'w', 'utf-8') as f:  # type: ignore
                f.write(output)
        except (IOError, OSError) as err:
            logger.warning("error writing file %s: %s", outfilename, err)

    def finish(self):
        # type: () -> None
        pass
