#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Created by Andre Anjos <andre.dos.anjos@cern.ch>
# Ter 02 Mar 2010 17:14:14 CET 

"""Tags to help coding your templates.
"""

from django import template
register = template.Library()
from djpro.models import *

@register.inclusion_tag('djpro/embed/list.html')
def djpro_list(max_projects=0, compact=False):
  objects = list(Project.objects.order_by('name'))
  objects.sort(cmp=lambda a, b: cmp(a.updated,b.updated), reverse=True)
  if max_projects > 0: objects = objects[:max_projects] 
  return {'projects': objects, 'compact': compact}


