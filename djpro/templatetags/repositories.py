#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Created by Andre Anjos <andre.dos.anjos@cern.ch>
# Fri 17 Oct 09:36:48 2008 

"""Tags to help coding your templates.
"""

from datetime import datetime
import os
from djpro.conf import settings
from djpro.utils import relative_date as rd_function
from djpro.utils import blob_is_text

from django import template
register = template.Library()
 
@register.filter("name")
def name(value):
    return os.path.dirname(value.replace(settings.DJPRO_GIT_BASE_DIRECTORY + os.sep, '', 1))

@register.filter("first_eight")
def first_eight(value):
  return "".join(list(str(value))[:8])

@register.filter("tuple_to_date")
def tuple_to_date(value):
  return datetime(*value[0:7])

@register.filter("relative_date")
def relative_date(value):
   return rd_function(datetime(*value[0:7]))

@register.filter("is_text")
def is_text(value):
  return blob_is_text(value)
