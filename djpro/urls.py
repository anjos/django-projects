from django.conf.urls.defaults import *
from django.views.generic import list_detail
from django.views.generic.simple import redirect_to
from djpro.models import Project, Download
from djpro.feeds import * 
from djpro.views import *
import djit.urls

feeds = dict()
feeds[LatestDownloadsForProject.basename] = LatestDownloadsForProject
feeds[LatestDeveloperDownloadsForProject.basename] = \
    LatestDeveloperDownloadsForProject 

all_feeds = dict(feeds)
all_feeds[SparkleUpdatesForProject.basename] = SparkleUpdatesForProject

download_detail = { 'queryset': Download.objects.filter(),
                    'template_name': 'djpro/download_detail.html',
                  }

notes_detail = { 'queryset': Download.objects.filter(),
                 'template_name': 'djpro/notes_detail.html',
               }

urlpatterns = patterns('',

  url(r'^$', project_list, name='list'),

  url(r'^feeds/(?P<url>.*)/$', 
      'django.contrib.syndication.views.feed',
      {'feed_dict': all_feeds},
      name='feeds'),

  # a PyPI-like index for easy-install and pip
  url(r'^pypi/$', pypi_index, name='pypi-index'),

  url(r'^pypi/(?P<slug>[-\w]+)/$', pypi_package, name='pypi-package'), 

  url(r'^pypi/simple/$', redirect_to, {'url': '/git/simple/'}),

  # other urls
  url(r'^(?P<slug>[-\w]+)/$', 
      project_detail, 
      { 'feeds': feeds.values(), }, 
      name='view-project'), 

  url(r'^(?P<slug>[-\w]+)/dsakey/$', 
      projects_dsa_pubkey, 
      name='dsakey'),

  url(r'^(?P<object_id>\d+)/download/$',
      list_detail.object_detail, 
      download_detail,
      name='download'),  

  url(r'^(?P<object_id>\d+)/notes/$',
      list_detail.object_detail,
      notes_detail,
      name='note'),

)

namespaced = (urlpatterns, 'djpro', 'djpro')

