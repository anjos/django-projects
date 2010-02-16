#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Created by Andre Anjos <andre.dos.anjos@cern.ch>
# Fri 17 Oct 09:36:48 2008 

"""Tags to help coding your templates.
"""

from django import template
register = template.Library()
from djpro.conf import settings
from djpro.utils import *

def repo_media(context):
  context["pygments_theme"] = settings.DJPRO_HIGHLIGHT_STYLE
  return context
register.inclusion_tag('djpro/embed/media.html', takes_context=True)(repo_media)

@register.inclusion_tag('djpro/embed/summary_bubble.html')
def summary_bubble(repo):
  return {'repo': repo}

@register.inclusion_tag('djpro/embed/tag_bubble.html')
def tag_bubble(repo, max_tags=0):
  tags = repo.tags
  tags.reverse()
  if max_tags > 0: tags = tags[:max_tags]
  return {'repo': repo, 'tags': tags}

@register.inclusion_tag('djpro/embed/list_bubble.html')
def list_bubble(max_repos=0):
  repos = get_repos()
  repos.sort(cmp=cmp_repo_changed, reverse=True)
  if max_repos > 0: repos = repos[:max_repos] 
  return {'repos': repos,}

@register.inclusion_tag('djpro/embed/shortlog.html')
def shortlog(repo, head, commits):
  return {'repo': repo, 'head': head, 'commits': commits}

@register.inclusion_tag('djpro/embed/commit_summary_bubble.html')
def commit_summary_bubble(repo, commit):
  return {'repo': repo, 'commit': commit}

@register.inclusion_tag('djpro/embed/statistics_bubble.html')
def statistics_bubble(commit):
  return {'commit': commit}

@register.inclusion_tag('djpro/embed/changes_bubble.html')
def changes_bubble(repo, commit):
  return {'repo': repo, 'commit': commit}

@register.inclusion_tag('djpro/embed/view_bubble.html')
def view_bubble(repo, commit, blob):
  return {'repo': repo, 'commit': commit, 'blob': blob}

@register.inclusion_tag('djpro/embed/diff_bubble.html')
def diff_bubble(diffs):
  return {'diffs': diffs}

@register.inclusion_tag('djpro/embed/tree_bubble.html')
def tree_bubble(repo, commit, tree, path):
  return {'repo': repo, 'commit': commit, 'tree': tree, 'path': path}

@register.inclusion_tag('djpro/embed/navigation.html')
def navigation(repo, commit):
  return {'repo': repo, 'commit': commit} 

@register.inclusion_tag('djpro/embed/history_bubble.html')
def history_bubble(repo, path, latest, commits):
  return {'repo': repo, 'path': path, 'latest': latest, 'commits': commits} 

