#!/usr/bin/env python

__author__ = "Abhinav Sarkar"
__version__ = "0.1"
__license__ = "GNU Lesser General Public License"

METADATA = dict(
	name='lastfm',
	version='0.1a',
	description="a pure python interface to the Last.fm Webservices API",
	long_description="a pure python interface to the Last.fm Webservices API",
	author="Abhinav Sarkar",
	author_email="abhinav.sarkar@gmail.com",
	maintainer="Abhinav Sarkar",
	maintainer_email="abhinav.sarkar@gmail.com",
	url="http://code.google.com/p/python-lastfm/downloads/list/",
	download_url="http://python-lastfm.googlecode.com/files/lastfm-0.1.tar.gz",
	package_dir = {'':'src'},
	packages=['lastfm'],
	license="GNU Lesser General Public License",
	keywords="audioscrobbler webservice api last.fm",
)

SETUPTOOLS_METADATA = dict(
	install_requires = ['setuptools', 'vobject'],
	include_package_data = True,
	classifiers = [
		'Development Status :: 3 - Alpha',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Topic :: Software Development :: Libraries :: Python Modules',
		'Topic :: Multimedia :: Sound/Audio',
		'Topic :: Internet',
	],
)

import sys
if sys.version < '2.5':
	SETUPTOOLS_METADATA['install_requires'].append('ElementTree')
	SETUPTOOLS_METADATA['install_requires'].append('cElementTree')

def Main():
  # Use setuptools if available, otherwise fallback and use distutils
  try:
    import setuptools
    METADATA.update(SETUPTOOLS_METADATA)
    setuptools.setup(**METADATA)
  except ImportError:
    import distutils.core
    distutils.core.setup(**METADATA)

if __name__ == '__main__':
  Main()