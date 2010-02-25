#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Created by Andre Anjos <andre.dos.anjos@cern.ch>
# Fri 17 Oct 09:36:48 2008 

"""Utitilies to retrieve repositories and management info.
"""

import os, re
from git import *
from conf import settings
import datetime, dateutils
from django.utils.translation import ugettext as _
from django.utils.translation import string_concat as _cat
from django.utils.translation import ungettext as _n
from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import smart_str, force_unicode
from django.utils.safestring import mark_safe
from django.conf import settings as django_settings

# setup the time zone once for comparison functions
import pytz
TZ = pytz.timezone(getattr(django_settings, 'TIME_ZONE', 'UTC'))

def tuple_to_date(d):
  """Returns a datetime object from the weird's git date/time output."""
  return datetime.datetime(d[0], d[1], d[2], d[3], d[4], d[5], 0, pytz.UTC)

def cmp_repo_changed(r1, r2):
  """Compares two repositories w.r.t. their last changed date. Older first."""
  return cmp(r1.commits()[0].committed_date, r2.commits()[0].committed_date)

def is_git_repo(d):
  """Tells if a certain directory is a readable git repository."""
  candidate = os.path.join(d, '.git')
  return os.path.exists(candidate) and os.access(candidate, os.R_OK)

def get_repo_paths(path, match=None, recursive=True):
  """Returns all git repositories found under the given "path"."""
  
  match_re = None
  if match: match_re = re.compile(match)

  retval = []

  if recursive:
    for root, dirs, files in os.walk(path):
      for d in dirs:
        repo = os.path.join(root, d)
        if is_git_repo(repo) and (match_re is None or match_re.search(d)):
          retval.append((repo, repo.replace(path + os.sep, '', 1)))
  else:
    try:
      for d in os.listdir(path):
        repo = os.path.join(path, d)
        if is_git_repo(repo) and (match_re is None or match_re.search(d)):
          retval.append((repo, d))
    except OSError:
      pass

  return retval

def get_repo(name):
  repo_path = os.path.join(settings.DJPRO_GIT_BASE_DIRECTORY, name)
  if os.path.isdir(repo_path):
    try:
      return Repo(repo_path)
    except Exception:
      pass
  return None

def get_repos(match=None, recursive=True):
  return [get_repo(k[1]) for k in \
      get_repo_paths(settings.DJPRO_GIT_BASE_DIRECTORY, match, recursive)]

def get_head(repo, name):
  for k in repo.heads:
    if k.name == name: return k
  return repo.heads[0] #should be the default head

def get_blob(tree, path):
  if not path: return None # there is no blob without a path

  # the double means: (path, git object)
  retval = [('', tree)]

  for k in path.split(os.sep):
    t = tree.get(k)
    if isinstance(t, Tree):
      retval.append((k, t))
      tree = t
    elif isinstance(t, Blob):
      retval.append((k, t))
      return retval
    else:
      break #no point in continuing, path does not exist!
  return None

def get_tree(tree, path):
  # the double means: (path, git tree)
  retval = [('', tree)]

  if not path: return retval # return the root directory

  for k in path.split(os.sep):
    t = tree.get(k)
    if isinstance(t, Tree):
      retval.append((k, t))
      tree = t
    else:
      return None #no point in continuing, path does not exist!
  return retval

def relative_date(t):
  d = dateutils.relativedelta(datetime.datetime.now(TZ), t)
  if d.years: 
    return _n(u'%(c)d year ago', u'%(c)d years ago', d.years) % {'c': d.years }
  if d.months: 
    return _n(u'%(c)d month ago', u'%(c)d months ago', d.months) % {'c': d.months }
  if d.days: 
    return _n(u'%(c)d day ago', u'%(c)d days ago', d.days) % {'c': d.days }
  if d.hours: 
    return _n(u'%(c)d hour ago', u'%(c)d hours ago', d.hours) % {'c': d.hours }
  if d.minutes: 
    return _n(u'%(c)d minute ago', u'%(c)d minutes ago', d.minutes) % {'c': d.minutes }
  if d.seconds: 
    return _n(u'%(c)d second ago', u'%(c)d seconds ago', d.seconds) % {'c': d.seconds }

  return _(u'just now')

def blob_is_text(blob):
  return blob.mime_type and (blob.mime_type.split('/')[0] == 'text')

def simple_html(value):
  """Returns simple html and mark it safe."""
  return mark_safe(force_unicode(value))

def simple_text(value):
  """Wraps text in a simple <pre> blob."""
  return simple_html('<pre>' + value + '</pre>')

def textile(value):
  """Converts the text data into html using textile"""
  try:
    import textile
  except ImportError:
    if django_settings.DEBUG: raise
    return simple_text('[warning: textile is *not* available]\n' + value) 
  else:
    return simple_html(textile.textile(smart_str(value), encoding='utf-8', output='utf-8'))

def restructuredtext(value):
  """Converts the text data into html using docutils"""
  try:
    from docutils.core import publish_parts
  except ImportError:
    if settings.DEBUG: raise
    return simple_text('[warning: docutils is *not* available]\n\n' + value) 
  else:
    docutils_settings = getattr(django_settings, 
        "RESTRUCTUREDTEXT_FILTER_SETTINGS", {})
    parts = publish_parts(source=smart_str(value), writer_name="html4css1", 
        settings_overrides=docutils_settings)
    return simple_html(parts["fragment"])

