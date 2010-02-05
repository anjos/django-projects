#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Created by Andre Anjos <andre.dos.anjos@cern.ch>
# Fri 17 Oct 09:36:48 2008 

"""Tags to help coding your templates.
"""

from django import template
register = template.Library()
from djpro.conf import settings

def repo_media(context):
  context["pygments_theme"] = settings.DJPRO_HIGHLIGHT_STYLE
  return context
register.inclusion_tag('djpro/embed/repo_media.html', takes_context=True)(repo_media)

def repo(context):
  return context
register.inclusion_tag('djpro/embed/repo.html', takes_context=True)(repo)

def repo_blob(context): return context
register.inclusion_tag('djpro/embed/repo_blob.html', takes_context=True)(repo_blob)

def repo_commit(context): return context
register.inclusion_tag('djpro/embed/repo_commit.html', takes_context=True)(repo_commit)

def repo_diff(context): return context
register.inclusion_tag('djpro/embed/repo_diff.html', takes_context=True)(repo_diff)

def repo_history(context): return context
register.inclusion_tag('djpro/embed/repo_history.html', takes_context=True)(repo_history)

def repo_list(context): return context
register.inclusion_tag('djpro/embed/repo_list.html', takes_context=True)(repo_list)

def repo_tree(context): return context
register.inclusion_tag('djpro/embed/repo_tree.html', takes_context=True)(repo_tree)

@register.inclusion_tag('djpro/embed/summary_bubble.html')
def summary_bubble(repo):
  return {'repo': repo}

@register.inclusion_tag('djpro/embed/tag_bubble.html')
def tag_bubble(repo):
  return {'repo': repo}

@register.inclusion_tag('djpro/embed/shortlog.html')
def shortlog(repo, head, commits):
  return {'repo': repo, 'head': head, 'commits': commits}

@register.inclusion_tag('djpro/embed/repo_summary.html')
def repo_summary(repo):
  return {'repo': repo}

