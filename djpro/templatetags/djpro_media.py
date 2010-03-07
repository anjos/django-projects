#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Created by Andre Anjos <andre.dos.anjos@cern.ch>
# Qua 17 Fev 2010 13:46:38 CET 

"""Media includes for the repositories and projects.
"""

from django import template
register = template.Library()
from djpro.conf import settings

@register.inclusion_tag('djpro/embed/media_bubble.html')
def djpro_bubble_media(url=settings.settings.MEDIA_URL): 
  return {'MEDIA_URL': url}
