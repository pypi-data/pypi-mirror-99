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

Consists of a *server* that is ready to run
Serve and the DAV package that provides WebDAV server(!) functionality.

Currently supports

    * WebDAV level 1
    * Level 2 (LOCK, UNLOCK)
    * Experimental iterator support

It plays nice with

    * Mac OS X Finder
    * Windows Explorer
    * iCal
    * cadaver
    * Nautilus

This package does *not* provide client functionality.

Installation
============

After installation of this package you will have a new script in you
$PYTHON/bin directory called *davserver*. This serves as the main entry point
to the server.

Examples
========

Example (using pip)::

    pip install PyWebDAV3
    davserver -D /tmp -n

Example (unpacking file locally)::

    tar xvzf PyWebDAV3-$VERSION.tar.gz
    cd pywebdav
    python setup.py develop
    davserver -D /tmp -n

For more information: https://github.com/andrewleech/PyWebDAV3

Changes
=======

%s
""" % CHANGES

setup(name='m9s-PyWebDAV3',
      description=pywebdav.__doc__,
      author=pywebdav.__author__,
      author_email=pywebdav.__email__,
      maintainer=pywebdav.__author__,
      maintainer_email=pywebdav.__email__,
      url='https://github.com/andrewleech/PyWebDAV3',
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
      keywords=['webdav',
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
      test_requires = ['pytest']
      )
