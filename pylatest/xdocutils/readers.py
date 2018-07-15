# -*- coding: utf8 -*-

"""
Pylatest ReStructuredText Readers module.
"""

# Copyright (C) 2018 Martin Bukatovič <martin.bukatovic@gmail.com>
# Copyright (C) 2017 mbukatov@redhat.com
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


from docutils.readers import standalone
from docutils.transforms import frontmatter

from pylatest.xdocutils.transforms import TestActionsTableTransform
from pylatest.xdocutils.transforms import TestActionsPlainIdTransform


class NoPlainReader(standalone.Reader):
    """
    NoPlainReader extends docutils standalone ReStructuredText reader
    to add few transformation to make the output human readable, everything
    else remains the same.
    """

    def get_transforms(self):
        transforms = standalone.Reader.get_transforms(self)
        transforms.append(TestActionsTableTransform)
        return transforms


class PlainReader(standalone.Reader):
    """
    PlainReader extends docutils standalone ReStructuredText reader
    to add few transformation to produce machine readable output, everything
    else remains the same.
    """

    def get_transforms(self):
        transforms = standalone.Reader.get_transforms(self)
        transforms.append(TestActionsPlainIdTransform)
        return transforms


class NoDocInfoReader(standalone.Reader):
    """
    NoDocInfoReader extends docutils standalone ReStructuredText reader
    to drop DocInfo transformation, everything else remains the same.

    This reader is used for unit testing only.
    """

    def get_transforms(self):
        transforms = standalone.Reader.get_transforms(self)
        transforms.remove(frontmatter.DocInfo)
        return transforms
