# -*- coding: utf-8 -*-
"""
Sphinx unit test driver module, copied without modifications (with exception of
this docstring and copying notice) from ``tests/run.py`` file of Sphinx
project, commit 139e09d12023a255b206c1158487d215217be920.

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


from __future__ import print_function

import os
import sys
import warnings
import traceback

from path import path

testroot = os.path.dirname(__file__) or '.'
sys.path.insert(0, os.path.abspath(os.path.join(testroot, os.path.pardir)))

# filter warnings of test dependencies
warnings.filterwarnings('ignore', category=DeprecationWarning, module='site')  # virtualenv
warnings.filterwarnings('ignore', category=ImportWarning, module='backports')
warnings.filterwarnings('ignore', category=ImportWarning, module='pkgutil')
warnings.filterwarnings('ignore', category=ImportWarning, module='pytest_cov')
warnings.filterwarnings('ignore', category=PendingDeprecationWarning, module=r'_pytest\..*')

# check dependencies before testing
print('Checking dependencies...')
for modname in ('pytest', 'mock', 'six', 'docutils', 'jinja2', 'pygments',
                'snowballstemmer', 'babel', 'html5lib'):
    try:
        __import__(modname)
    except ImportError as err:
        if modname == 'mock' and sys.version_info[0] == 3:
            continue
        traceback.print_exc()
        print('The %r package is needed to run the Sphinx test suite.' % modname)
        sys.exit(1)

# find a temp dir for testing and clean it up now
os.environ['SPHINX_TEST_TEMPDIR'] = \
    os.path.abspath(os.path.join(testroot, 'build')) \
    if 'SPHINX_TEST_TEMPDIR' not in os.environ \
    else os.path.abspath(os.environ['SPHINX_TEST_TEMPDIR'])
tempdir = path(os.environ['SPHINX_TEST_TEMPDIR'])
print('Temporary files will be placed in %s.' % tempdir)
if tempdir.exists():
    tempdir.rmtree()
tempdir.makedirs()

print('Running Sphinx test suite (with Python %s)...' % sys.version.split()[0])
sys.stdout.flush()

# exclude 'root' and 'roots' dirs for pytest test collector
ignore_paths = [
    os.path.relpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), sub))
    for sub in ('root', 'roots')
]
args = sys.argv[1:]
for ignore_path in ignore_paths:
    args.extend(['--ignore', ignore_path])

import pytest  # NOQA
sys.exit(pytest.main(args))
