#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Created by Andre Anjos <andre.dos.anjos@cern.ch>
# Fri 17 Oct 09:36:48 2008 

"""Specialized views for projects.
"""

from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.core.exceptions import ObjectDoesNotExist
from djpro.models import Project, Download
from django.template import RequestContext

from utils import *
from conf import settings

def projects_dsa_pubkey(request, slug):
  """View the DSA public key of project as a downloadable file"""
  try:
    p = Project.objects.get(slug=slug)
  except: 
    raise ObjectDoesNotExist

  return HttpResponse(p.dsa_pubkey, mimetype="text/plain")

def repo_list(request, template_name='djpro/repo_list.html'):
  return render_to_response(template_name, 
                            {'repos': get_repos(),},
                            context_instance=RequestContext(request))

def repo_detail(request, template_name='djpro/repo.html'):
  if not request.GET.has_key('r'): return repo_list(request) 
  r = get_repo(request.GET['r'])
  c = r.commits(max_count=r.commit_count()) 

  return render_to_response(template_name, 
      {'repo': r, 'commits': c}, 
      context_instance=RequestContext(request))

def repo_history(request, commit=None, template_name='djpro/repo_history.html'):
  if not request.GET.has_key('r'): raise ObjectDoesNotExist 
  if not request.GET.has_key('b'): raise ObjectDoesNotExist

  p = request.GET['b']
  r = get_repo(request.GET['r'])

  commits = r.log(path=p) 

  if commit: #if I need to start from a specific commit and go backwards...
    index = 0
    for k in commits:
      if commit == k.id: break
      ++index
    commits = commits[index:]

  diffs = []
  for k in commits:
    diffs.extend([d for d in k.diffs if d.b_path and d.b_path.find(p) == 0])

  while diffs[-1].renamed and diffs[-1].a_path: #track down renames
    p = diffs[-1].a_path
    commits_ext = r.log(path=p)
    diffs_ext = []
    for k in commits_ext:
      diffs_ext.extend([d for d in k.diffs if d.b_path and d.b_path.find(p) == 0])
    commits.extend(commits_ext)
    diffs.extend(diffs_ext)

  return render_to_response(template_name, 
      {'repo': r, 
       'commits': zip(commits, diffs),
       'path': p}, 
      context_instance=RequestContext(request))

def repo_commit(request, commit, template_name='djpro/repo_commit.html'):
  if not request.GET.has_key('r'): raise ObjectDoesNotExist 
  r = get_repo(request.GET['r'])
  return render_to_response(template_name, 
                            {
                             'repo': r, 
                             'commit': r.commit(commit),
                            }, 
                            context_instance=RequestContext(request))

def repo_diff(request, commit, template_name='djpro/repo_diff.html'):
  if not request.GET.has_key('r'): raise ObjectDoesNotExist 
  r = get_repo(request.GET['r'])
  c = r.commit(commit) 
  d = c.diffs
  if request.GET.has_key('b'): #only interested in subset
    p = request.GET['b']
    keep = [k for k in d if k.b_path.find(p) == 0]
    d = keep
     
  return render_to_response(template_name, 
                            {
                             'repo': r, 
                             'commit': c, 
                             'diffs': d,
                            }, 
                            context_instance=RequestContext(request))

def download_tree(request, commit=None):
  if not request.GET.has_key('r'): raise ObjectDoesNotExist 
  r = get_repo(request.GET['r'])
  if commit: 
    c = r.commit(commit)
    root = r.commit(commit).tree
  else: 
    head = get_head(r, request.GET.get('h', None))
    c = head.commit
    root = r.tree()
  p = request.GET.get('t', '').strip(' ' + os.sep)
  t = get_tree(root, p)
  if not t: raise ObjectDoesNotExist
  t = t[-1][1] # we only need the last object of the returned chain
  
  data = r.archive_tar_gz(t.id)
   
  retval = HttpResponse(data, mimetype='application/x-tar-gz')
  filename = t.name
  if not filename: filename = os.path.basename(r.wd)
  retval['Content-Disposition'] = 'attachment; filename=%s.tar.gz' % filename 
  return retval

def repo_tree(request, commit=None, template_name='djpro/repo_tree.html'):
  if not request.GET.has_key('r'): raise ObjectDoesNotExist 
  r = get_repo(request.GET['r'])
  if commit: 
    c = r.commit(commit)
    root = r.commit(commit).tree
  else: 
    head = get_head(r, request.GET.get('h', None))
    c = head.commit
    root = r.tree()
  p = request.GET.get('t', '').strip(' ' + os.sep)
  t = get_tree(root, p)
  if not t: raise ObjectDoesNotExist
   
  return render_to_response(template_name, 
                            {
                             'repo': r, 
                             'tree': t, 
                             'path': p,
                             'commit': c, 
                            }, 
                            context_instance=RequestContext(request))

def raw_blob(b):
  retval = HttpResponse(b.data, mimetype=b.mime_type)
  retval['Content-Disposition'] = 'attachment; filename=%s' % b.basename
  return retval

def find_blob(repo, path, head=None, commit=None):
  if not repo: raise ObjectDoesNotExist
  if not path: raise ObjectDoesNotExist
  r = get_repo(repo)
  if commit:
    c = r.commit(commit)
    root = r.commit(commit).tree
  else:
    head = get_head(r, head)
    c = head.commit
    root = r.tree() 
  b = get_blob(root, path.strip(' ' + os.sep))
  if not b: raise ObjectDoesNotExist
  return (r, c, b)

def repo_raw(request, commit=None):
  (r, c, b) = find_blob(request.GET.get('r', None), request.GET.get('b', None),
            request.GET.get('h', None), commit)
  return raw_blob(b[-1][1])

def repo_blob(request, commit=None, template_name='djpro/repo_blob.html'):
  (r, c, b) = find_blob(request.GET.get('r', None), request.GET.get('b', None),
            request.GET.get('h', None), commit)
  if not blob_is_text(b[-1][1]): return raw_blob(b[-1][1])

  return render_to_response(template_name, 
                            {
                             'repo': r, 
                             'blob': b, 
                             'commit': c, 
                            }, 
                            context_instance=RequestContext(request))

