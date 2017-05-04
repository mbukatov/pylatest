# -*- coding: utf-8 -*-
"""
Sphinx path module, copied without modifications (with exception of this
docstring and copying notice) from ``tests/path.py`` file of Sphinx project,
commit 139e09d12023a255b206c1158487d215217be920.

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
import sys
import shutil
from io import open

from six import PY2, text_type


FILESYSTEMENCODING = sys.getfilesystemencoding() or sys.getdefaultencoding()


class path(text_type):
    """
    Represents a path which behaves like a string.
    """
    if PY2:
        def __new__(cls, s, encoding=FILESYSTEMENCODING, errors='strict'):
            if isinstance(s, str):
                s = s.decode(encoding, errors)
                return text_type.__new__(cls, s)
            return text_type.__new__(cls, s)

    @property
    def parent(self):
        """
        The name of the directory the file or directory is in.
        """
        return self.__class__(os.path.dirname(self))

    def basename(self):
        return os.path.basename(self)

    def abspath(self):
        """
        Returns the absolute path.
        """
        return self.__class__(os.path.abspath(self))

    def isabs(self):
        """
        Returns ``True`` if the path is absolute.
        """
        return os.path.isabs(self)

    def isdir(self):
        """
        Returns ``True`` if the path is a directory.
        """
        return os.path.isdir(self)

    def isfile(self):
        """
        Returns ``True`` if the path is a file.
        """
        return os.path.isfile(self)

    def islink(self):
        """
        Returns ``True`` if the path is a symbolic link.
        """
        return os.path.islink(self)

    def ismount(self):
        """
        Returns ``True`` if the path is a mount point.
        """
        return os.path.ismount(self)

    def rmtree(self, ignore_errors=False, onerror=None):
        """
        Removes the file or directory and any files or directories it may
        contain.

        :param ignore_errors:
            If ``True`` errors are silently ignored, otherwise an exception
            is raised in case an error occurs.

        :param onerror:
            A callback which gets called with the arguments `func`, `path` and
            `exc_info`. `func` is one of :func:`os.listdir`, :func:`os.remove`
            or :func:`os.rmdir`. `path` is the argument to the function which
            caused it to fail and `exc_info` is a tuple as returned by
            :func:`sys.exc_info`.
        """
        shutil.rmtree(self, ignore_errors=ignore_errors, onerror=onerror)

    def copytree(self, destination, symlinks=False):
        """
        Recursively copy a directory to the given `destination`. If the given
        `destination` does not exist it will be created.

        :param symlinks:
            If ``True`` symbolic links in the source tree result in symbolic
            links in the destination tree otherwise the contents of the files
            pointed to by the symbolic links are copied.
        """
        shutil.copytree(self, destination, symlinks=symlinks)

    def movetree(self, destination):
        """
        Recursively move the file or directory to the given `destination`
        similar to the  Unix "mv" command.

        If the `destination` is a file it may be overwritten depending on the
        :func:`os.rename` semantics.
        """
        shutil.move(self, destination)

    move = movetree

    def unlink(self):
        """
        Removes a file.
        """
        os.unlink(self)

    def stat(self):
        """
        Returns a stat of the file.
        """
        return os.stat(self)

    def utime(self, arg):
        os.utime(self, arg)

    def open(self, mode='r', **kwargs):
        return open(self, mode, **kwargs)

    def write_text(self, text, encoding='utf-8', **kwargs):
        """
        Writes the given `text` to the file.
        """
        if isinstance(text, bytes):
            text = text.decode(encoding)
        with open(self, 'w', encoding=encoding, **kwargs) as f:
            f.write(text)

    def text(self, encoding='utf-8', **kwargs):
        """
        Returns the text in the file.
        """
        mode = 'rU' if PY2 else 'r'
        with open(self, mode=mode, encoding=encoding, **kwargs) as f:
            return f.read()

    def bytes(self):
        """
        Returns the bytes in the file.
        """
        with open(self, mode='rb') as f:
            return f.read()

    def write_bytes(self, bytes, append=False):
        """
        Writes the given `bytes` to the file.

        :param append:
            If ``True`` given `bytes` are added at the end of the file.
        """
        if append:
            mode = 'ab'
        else:
            mode = 'wb'
        with open(self, mode=mode) as f:
            f.write(bytes)

    def exists(self):
        """
        Returns ``True`` if the path exist.
        """
        return os.path.exists(self)

    def lexists(self):
        """
        Returns ``True`` if the path exists unless it is a broken symbolic
        link.
        """
        return os.path.lexists(self)

    def makedirs(self, mode=0o777):
        """
        Recursively create directories.
        """
        os.makedirs(self, mode)

    def joinpath(self, *args):
        """
        Joins the path with the argument given and returns the result.
        """
        return self.__class__(os.path.join(self, *map(self.__class__, args)))

    def listdir(self):
        return os.listdir(self)

    __div__ = __truediv__ = joinpath

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, text_type.__repr__(self))
