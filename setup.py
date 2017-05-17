# -*- coding: utf8 -*-
"""
A setuptools based setup module for Pylatest.

See:

* https://packaging.python.org/en/latest/distributing.html
* https://github.com/pypa/sampleproject
"""


from setuptools import setup, find_packages
import codecs
import os


long_description="""\
Pylatest project consists of set of Docutils/Sphinx extensions and related
tools which allows you to:

* Write a description of a test case using reStructuredText syntax.
* Maintain test case description as Sphinx project.
* Include this description into a python source code directly, where it can
  be split into individual sections or actions to be performed, so that the
  description and test automation code are stored next to each other.

The reason behind this is to make synchronization between automatic test cases
and test case description documents simple while keeping the maintenance cost
low in the long term.
"""

setup(
    name='pylatest',
    # See https://packaging.python.org/en/latest/distributing/#choosing-a-versioning-scheme
    # TODO: connect with git tags?
    version='0.1.0',
    description='Testcase description management tools.',
    long_description=long_description,
    url='http://github.com/mbukatov/pylatest/',
    author='Martin Bukatovič',
    author_email='mbukatov@redhat.com',
    license='GPLv3',
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Utilities',
        'Topic :: Text Processing :: Markup',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        ],
    packages=find_packages(exclude=['doc', 'tests']),
    install_requires=['docutils', 'lxml', 'sphinx'],
    # TODO: make this work with git (and remove MANIFEST.in?)
    # setup_requires=['setuptools_scm'],
    # use_scm_version=True,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'pylatest-template=pylatest.template:main',
            'py2pylatest=pylatest.pysource:main',
            'pylatest-rst2html=pylatest.main:pylatest2html',
            'pylatest-rst2htmlplain=pylatest.main:pylatest2htmlplain',
            'pylatest-rst2pseudoxml=pylatest.main:pylatest2pseudoxml',
            'pylatest-preview=pylatest.main:pylatest_preview',
            'pylatest-quickstart=pylatest.xsphinx.quickstart:main',
        ],
    },
    )
