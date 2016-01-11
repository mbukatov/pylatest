# -*- coding: utf8 -*-
"""
A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""


from setuptools import setup, find_packages
import codecs
import os


here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with codecs.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pylatest',
    version='0.0.4',
    description='Testcase description generation tools.',
    long_description=long_description,
    url='http://github.com/mbukatov/pylatest/',
    author='Martin Bukatovič',
    author_email='mbukatov@redhat.com',
    license='GPLv3',
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Software Development :: Quality Assurance',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        ],
    packages=find_packages(exclude=['doc']),
    install_requires=['docutils'],
    package_data={'pylatest': ['templates/*']},
    scripts=[
        'bin/pylatest2html',
        'bin/pylatest2htmlplain',
        'bin/py2pylatest',
        'bin/pylatest-template'],
    )
