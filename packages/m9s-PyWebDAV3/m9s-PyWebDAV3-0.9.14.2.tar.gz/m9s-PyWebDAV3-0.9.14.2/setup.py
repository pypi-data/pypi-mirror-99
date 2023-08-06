#!/usr/bin/env python

from __future__ import absolute_import
from setuptools import setup, find_packages
from io import open
import os

import pywebdav

CHANGES = open(os.path.join(os.path.dirname(__file__), 'doc/Changes'), 'r', encoding='utf-8').read()

DOC = """\
WebDAV library for python3
==========================

Consists of a WebDAV server that is ready to run and serve the DAV package.
This package does *not* provide client functionality.

Currently supports

    * WebDAV level 1
    * Level 2 (LOCK, UNLOCK)
    * Experimental iterator support

The following clients are known to work

    * Mac OS X Finder
    * Windows Explorer
    * iCal
    * cadaver
    * Nautilus
    * Mozilla Thunderbird (Lightning)
    * Cadaver
    * Konqueror
    * Evolution
    * CarDAV-PHP
    * vCard-parser

Installation
============

After installation of this package you will have a new script in you
$PYTHON/bin directory called *davserver*. This serves as the main entry point
to the server.

Examples
========

Example (using pip)::

    pip install m9s-PyWebDAV3
    davserver -D /tmp -n

Example (unpacking file locally)::

    tar xvzf m9s-PyWebDAV3-$VERSION.tar.gz
    cd pywebdav
    python setup.py develop
    davserver -D /tmp -n

For more information: https://gitlab.com/m9s/webdav.git

This project was started as a fork of https://github.com/jaysonlarose/PyWebDAV3.git

Changes
=======

%s
""" % CHANGES

setup(name='m9s-PyWebDAV3',
    description=pywebdav.__doc__,
    author=pywebdav.__author__,
    author_email=pywebdav.__email__,
    maintainer='MBSolutions',
    maintainer_email='info@m9s.biz',
    project_urls={
            "Bug Tracker": 'https://support.m9s.biz/',
            "Source Code": 'https://gitlab.com/m9s/webdav.git',
            },
    platforms=['Unix', 'Windows'],
    license=pywebdav.__license__,
    version=pywebdav.__version__,
    long_description=DOC,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
    ],
    keywords=[
        'webdav',
        'Tryton',
        'GNUHealth',
        'server',
        'dav',
        'standalone',
        'library',
        'gpl',
        'http',
        'rfc2518',
        'rfc 2518'
        ],
    packages=find_packages(),
    zip_safe=False,
    entry_points={
        'console_scripts': ['davserver = pywebdav.server.server:run']
    },
    tests_require=['pytest'],
    )
