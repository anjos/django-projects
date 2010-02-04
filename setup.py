#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Created by Andre Anjos <andre.dos.anjos@cern.ch>
# Seg 14 Set 2009 14:42:06 CEST 

"""Installation instructions for djpro
"""

from setuptools import setup, find_packages

setup(

    name = "djpro",
    version = "0.1", 
    packages = find_packages(),

    # we also need all translation files and templates
    package_data = {
      'djpro': [
        'templates/djpro/*.html',
        'templates/djpro/feeds/*.html',
        'media/css/*.css',
        'media/img/*',
        'locale/*/LC_MESSAGES/django.po',
        'locale/*/LC_MESSAGES/django.mo',
        ],
      },

    zip_safe=False,

    install_requires = [
      'setuptools',
      'Django>=1.1',
      'docutils',
      'gitpython',
      'PIL>=1.1.6',
      'Pygments>=1.2',
      'dateutils',
      'textile',
      ],

    dependency_links = [
      'http://docutils.sourceforge.net/docutils-snapshot.tgz',
      ],

    # metadata for upload to PyPI
    author = "Andre Anjos",
    author_email = "andre.dos.anjos@gmail.com",
    description = "Provides a framework to manage software projects based on git",
    license = "PSF",
    keywords = "django software project git",
    url = "",   # project home page, if any
    
)

