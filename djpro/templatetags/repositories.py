#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Created by Andre Anjos <andre.dos.anjos@cern.ch>
# Fri 17 Oct 09:36:48 2008 

"""Tags to help coding your templates.
"""

from datetime import datetime
import os, stat
from djpro.conf import settings
from djpro.utils import relative_date as rd_function
from djpro.utils import blob_is_text
import git

from django import template
register = template.Library()
 
@register.filter("name")
def name(value):
  """Distils the repository name from a full repo path."""
  return os.path.dirname(value.replace(settings.DJPRO_GIT_BASE_DIRECTORY + os.sep, '', 1))

@register.filter("first_eight")
def first_eight(value):
  """Git the first 8 digits from git hashes."""
  return "".join(list(str(value))[:8])

@register.filter("tuple_to_date")
def tuple_to_date(value):
  """Returns a datetime object from the weird's git date/time output."""
  return datetime(*value[0:7])

@register.filter("relative_date")
def relative_date(value):
  """Calculates the relative date, style "1 week ago"."""
  return rd_function(datetime(*value[0:7]))

@register.filter("is_text")
def is_text(value):
  """Tells if a certain blob is text and can be displayed by a browser."""
  return blob_is_text(value)

@register.filter("is_tree")
def is_tree(value):
  return isinstance(value, git.Tree)

@register.filter("mode")
def mode(value):
  """Converts a numerical mode (see chmod) into a string representation."""
  retval = ''

  # basic file type interpretation
  value = int(value, 8) 
  if stat.S_ISDIR(value): retval += 'd'
  elif stat.S_ISLNK(value): retval += 'l'
  else: retval += '-'

  # checks for user permissions
  if value & stat.S_IRUSR: retval += 'r'
  else: retval += '-'
  if value & stat.S_IWUSR: retval += 'w'
  else: retval += '-'
  if value & stat.S_IXUSR: retval += 'x'
  else: retval += '-'

  # checks for group permissions
  if value & stat.S_IRGRP: retval += 'r'
  else: retval += '-'
  if value & stat.S_IWGRP: retval += 'w'
  else: retval += '-'
  if value & stat.S_IXGRP: retval += 'x'
  else: retval += '-'

  # checks for group permissions
  if value & stat.S_IROTH: retval += 'r'
  else: retval += '-'
  if value & stat.S_IWOTH: retval += 'w'
  else: retval += '-'
  if value & stat.S_IXOTH: retval += 'x'
  else: retval += '-'
  return retval

@register.simple_tag
def merge_path(path, extension):
  """Merges two paths with special attention to empty "path"s."""
  if not path: return extension
  return os.path.join(path, extension)

