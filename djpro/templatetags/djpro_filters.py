#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Created by Andre Anjos <andre.dos.anjos@cern.ch>
# Qua 24 Fev 2010 11:19:11 CET 

"""A list of filters for projects.
"""

from django import template
register = template.Library()
 
@register.filter("document")
def document(object, value):
  """Displays a document from this project, if it exists or nothing."""
  return object.document(value)

