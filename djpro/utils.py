#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Created by Andre Anjos <andre.dos.anjos@cern.ch>
# Fri 17 Oct 09:36:48 2008 

"""Utitilies to retrieve repositories and management info.
"""

import os, re
from git import *
from conf import settings

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
  name = name.replace('@', os.sep)
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

def get_commit(name, commit):
  repo = get_repo(name)
  return repo.commit(commit)

def get_blob(repo, commit, file):
    repo = get_repo(repo)
    commit = repo.commit(commit)
    tree = commit.tree
    for path_seg in file.split(os.sep):
        t = tree.get(path_seg)
        if isinstance(t, Tree):
            tree = t
        else:
            blob = t
    return blob
