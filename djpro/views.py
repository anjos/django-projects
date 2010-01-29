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

from pygments import highlight
from pygments.lexers import guess_lexer_for_filename
from pygments.formatters import HtmlFormatter

from utils import *
from conf import settings

def projects_dsa_pubkey(request, slug):
  """View the DSA public key of project as a downloadable file"""
  try:
    p = Project.objects.get(slug=slug)
  except: 
    raise ObjectDoesNotExist

  return HttpResponse(p.dsa_pubkey, mimetype="text/plain")

def repo_index(request, template_name='djpro/repo_index.html'):
  return render_to_response(template_name, 
                            {'repos': get_repos(),},
                            context_instance=RequestContext(request))

def repo(request, repo, template_name='djpro/repo.html'):
  return render_to_response(template_name, 
                            {'repo': get_repo(repo)}, 
                            context_instance=RequestContext(request))

def repo_commit(request, repo, commit, template_name='djpro/repo_commit.html'):
  return render_to_response(template_name, 
                            {'diffs': get_commit(repo, commit).diffs, 
                             'repo': get_repo(repo), 
                             'commit': commit, 
                            }, 
                            context_instance=RequestContext(request))

def repo_blob(request, repo, commit):
  file = request.GET.get('file', '')
  blob = get_blob(repo, commit, file)
  lexer = guess_lexer_for_filename(blob.basename, blob.data)
  return HttpResponse(highlight(blob.data, lexer, HtmlFormatter(cssclass="pygment_highlight", linenos='inline')))
