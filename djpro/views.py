#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Created by Andre Anjos <andre.dos.anjos@cern.ch>
# Fri 17 Oct 09:36:48 2008 

"""Specialized views for projects.
"""

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist
from djpro.models import Project, Download
from django.template import RequestContext
from django.contrib.sites.models import Site

from models import *

def project_list(request, template_name='djpro/list.html'):
  """Returns a project list."""

  objects = list(Project.objects.order_by('name'))
  objects.sort(cmp=lambda a, b: cmp(a.updated,b.updated), reverse=True)

  return render_to_response(template_name,
      { 'object_list': objects, 
      },
      context_instance=RequestContext(request))

def project_detail(request, slug, template_prefix='djpro/detail', **kwargs):

  object = Project.objects.get(vc__slug=slug)
  if PythonProject.objects.filter(vc__slug=slug): 
    # in this case we use our PyPI specialized view for Python projects
    return pypi_package(request, slug, **kwargs)
    
  elif MacProject.objects.filter(vc__slug=slug):
    object = object.macproject
    template_name = template_prefix + '_mac.html'
  else:
    # this is a simple project
    template_name = template_prefix + '.html'

  return render_to_response(template_name, 
      {'object': object,
       'feeds': kwargs['feeds'],
      },
      context_instance=RequestContext(request))

def projects_dsa_pubkey(request, slug):
  """View the DSA public key of project as a downloadable file"""
  try:
    p = Project.objects.get(vc__slug=slug)
  except: 
    raise ObjectDoesNotExist

  return HttpResponse(p.dsa_pubkey, mimetype="text/plain")

def pypi_index(request, template_name='djpro/pypi_index.html'):
  """Lists all the Python Projects available at this site.
  """
  objects = PythonProject.objects.order_by('name') 
  objects = [k for k in objects if k.vc.git.tags]
  return render_to_response(template_name, 
      { 'object_list': objects, 
        'site_domain': Site.objects.get_current().domain,
      },
      context_instance=RequestContext(request))

def pypi_package(request, slug, template_name='djpro/pypi_package.html',
    **kwargs):
  """Returns a single package page in the easy_install style. See documentation
  here: http://peak.telecommunity.com/DevCenter/EasyInstall#package-index-api
  """
  object = PythonProject.objects.get(vc__slug=slug)

  tags = object.vc.git.tags
  if tags: tarball = object.vc.git.archive_tar_gz(tags[-1].name)
  else: tarball = object.vc.git.archive_tar_gz() # gets the default head

  tags.reverse()
  return render_to_response(template_name, 
      { 
        'object': object,
        'tags': tags,
        'size': len(tarball),
      },
      context_instance=RequestContext(request))
