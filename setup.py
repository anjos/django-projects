#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Created by Andre Anjos <andre.dos.anjos@cern.ch>
# Seg 14 Set 2009 14:42:06 CEST 

"""Installation instructions for djpro
"""

from setuptools import setup, find_packages

setup(

    name = "djpro",
    version = "0.5", 
    packages = find_packages(),

    # we also need all translation files and templates
    package_data = {
      'djpro': [
        'templates/djpro/*.html',
        'templates/djpro/feeds/*.html',
        'templates/djpro/embed/*.html',
        'media/css/*.css',
        'media/img/*',
        'locale/*/LC_MESSAGES/django.po',
        'locale/*/LC_MESSAGES/django.mo',
        ],
      },

    zip_safe=False,

    install_requires = [
      'djit',
      'django',
      'docutils',
      'PIL',
      ],

    # metadata for upload to PyPI
    author = "Andre Anjos",
    author_email = "andre.dos.anjos@gmail.com",
    description = "Provides a framework to manage software projects based on git",
    license = "PSF",
    keywords = "django software project git",
    url = "",   # project home page, if any
    
)

