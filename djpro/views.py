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
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from utils import *
from conf import settings
from models import *
import hashlib

def project_detail(request, slug, **kwargs):

  object = Project.objects.get(slug=slug)
  r = get_repo(object.git_dir)
  head = request.GET.get('h', r.heads[0].name) # get default head
  c = r.commits(start=head, max_count=r.commit_count())
  paginator = Paginator(c, settings.DJPRO_COMMITS_PER_PAGE)

  try:
    page = int(request.GET.get('page', '1'))
  except ValueError:
    page = 1

  try:
    commits = paginator.page(page)
  except (EmptyPage, InvalidPage):
    commits = paginator.page(paginator.num_pages)
  
  return render_to_response(kwargs['template_name'], 
      {'object': object,
       'feeds': kwargs['feeds'],
       'repo': r, 
       'commits': commits, 
       'head': head,
       'max_tags': settings.DJPRO_MAX_TAGS}, 
      context_instance=RequestContext(request))

def projects_dsa_pubkey(request, slug):
  """View the DSA public key of project as a downloadable file"""
  try:
    p = Project.objects.get(slug=slug)
  except: 
    raise ObjectDoesNotExist

  return HttpResponse(p.dsa_pubkey, mimetype="text/plain")

def repo_list(request, template_name='djpro/repo_list.html'):
  repos = sorted(get_repos(), cmp=cmp_repo_changed, reverse=True)
  return render_to_response(template_name, 
                            {'repos': repos,},
                            context_instance=RequestContext(request))

def repo_detail(request, template_name='djpro/repo.html'):
  if not request.GET.has_key('r'): return repo_list(request) 
  r = get_repo(request.GET['r'])
  head = request.GET.get('h', r.heads[0].name) # get default head
  c = r.commits(start=head, max_count=r.commit_count())
  paginator = Paginator(c, settings.DJPRO_COMMITS_PER_PAGE)

  try:
    page = int(request.GET.get('page', '1'))
  except ValueError:
    page = 1

  try:
    commits = paginator.page(page)
  except (EmptyPage, InvalidPage):
    commits = paginator.page(paginator.num_pages)
  
  return render_to_response(template_name, 
      {'repo': r, 
       'commits': commits, 
       'head': head,
       'max_tags': settings.DJPRO_MAX_TAGS}, 
      context_instance=RequestContext(request))

def repo_history(request, commit=None, template_name='djpro/repo_history.html'):
  if not request.GET.has_key('r'): raise ObjectDoesNotExist 
  if not request.GET.has_key('b'): raise ObjectDoesNotExist

  p = request.GET['b'].strip(' ' + os.sep)
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

  # this little magic will generate a list that looks like this:
  # ['a', 'a/b', 'a/b/c', 'a/b/c/d' 'a/b/c/d/file.txt']
  path = p.split(os.sep)
  path = [os.sep.join(path[:(len(path)-k)]) for k in range(len(path))]
  path.reverse()

  return render_to_response(template_name, 
      {'repo': r, 
       'commits': zip(commits, diffs),
       'path': path,
       }, 
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

def download_tree(request, commit=None, filename=None):

  """Downloads any tree from a project."""
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

  if not filename:
    if t.name: filename = t.name
    else:
      filename = os.path.basename(r.wd).replace('.git','',1)
    filename += '-%s' % c.id[:8]

  retval['Content-Disposition'] = 'attachment; filename=%s.tar.gz' % filename 
  return retval

def download_release(request):
  """Downloads a particular tag or the head of a certain branch."""
  if not request.GET.has_key('r'): raise ObjectDoesNotExist
  r = get_repo(request.GET['r'])

  commit = None
  filename = None

  project_name = os.path.basename(r.wd).replace('.git','',1)
  if request.GET.has_key('tag'): #user chose a tag
    for k in r.tags: 
      if k.name == request.GET['tag']: #found tag
        return download_tree(request, commit=k.commit.id,
            filename=project_name + '-%s' % k.name)
  elif request.GET.has_key('head'): #user wants the head of a branch
    for k in r.heads:
      if k.name == request.GET['head']: #found tag
        return download_tree(request, commit=k.commit.id,
            filename=project_name + '-%s-head' % k.name)

  # if you get to this point the user has not provided a t or h tag, or we
  # could not find the referred tag or branch.
  raise ObjectDoesNotExist

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

def pypi_index(request, template_name='djpro/pypi_index.html'):
  """Returns a site package list in the easy_install style. See documentation
  here: http://peak.telecommunity.com/DevCenter/EasyInstall#package-index-api
  """
  objects = Project.objects.filter(python_project=True).order_by('slug') 
  objects = [k for k in objects if objects.get_repo().tags]
  return render_to_response(template_name, { 'object_list': objects },
      context_instance=RequestContext(request))

def pypi_package(request, slug, version=None, template_name='djpro/pypi_package.html'):
  """Returns a single package page in the easy_install style. See documentation
  here: http://peak.telecommunity.com/DevCenter/EasyInstall#package-index-api
  """
  object = Project.objects.get(slug=slug)
  if version: tarball = object.repo().archive_tar_gz(version)
  else: tarball = object.repo().archive_tar_gz(object.repo().tags[-1].name)
  md5 = hashlib.md5()
  md5.update(tarball)
  return render_to_response(template_name, 
      { 
        'object': object,
        'version': version,
        'size': len(tarball),
        'md5': md5.hexdigest()
      },
      context_instance=RequestContext(request))
