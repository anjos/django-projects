#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Created by Andre Anjos <andre.dos.anjos@cern.ch>
# Fri 17 Oct 09:36:48 2008 

"""Tags to help coding your templates.
"""

from datetime import datetime
import os
from djpro.conf import settings

from django import template
register = template.Library()
 
@register.filter("name")
def name(value):
    return os.path.dirname(value.replace(settings.DJPRO_GIT_BASE_DIRECTORY + os.sep, '', 1))

@register.filter("mangled")
def name(value):
    return os.path.dirname(value.replace(settings.DJPRO_GIT_BASE_DIRECTORY + os.sep, '', 1)).replace(os.sep, '@')

@register.filter("first_eight")
def first_eight(value):
  return "".join(list(str(value))[:8])

@register.filter("tuple_to_date")
def tuple_to_date(value):
  return datetime(*value[0:7])
