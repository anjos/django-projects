from django.conf.urls.defaults import *
from django.views.generic import list_detail
from djpro.models import Project, Download
from djpro.feeds import * 
from djpro.views import *

feeds = dict()
feeds[LatestDownloadsForProject.basename] = LatestDownloadsForProject
feeds[LatestDeveloperDownloadsForProject.basename] = \
    LatestDeveloperDownloadsForProject 

all_feeds = dict(feeds)
all_feeds[SparkleUpdatesForProject.basename] = SparkleUpdatesForProject

project_list = { 'queryset': Project.objects.order_by('-date'),
                 'template_name': 'djpro/list.html',
               }

project_detail = { 'queryset': Project.objects.filter(),
                   'template_name': 'djpro/detail.html',
                   'extra_context': {'feeds': feeds.values()},
                 }

download_detail = { 'queryset': Download.objects.filter(),
                    'template_name': 'djpro/download_detail.html',
                  }

notes_detail = { 'queryset': Download.objects.filter(),
                 'template_name': 'djpro/notes_detail.html',
               }

urlpatterns = patterns('',
                       url(r'^$', list_detail.object_list, project_list,
                           name='list'),
                       url(r'^feeds/(?P<url>.*)/$', 
                           'django.contrib.syndication.views.feed',
                           {'feed_dict': all_feeds},
                           name='feeds'),
                       url(r'^dsakey/(?P<slug>\w+)/$', 
                           projects_dsa_pubkey, name='dsakey'),
                       url(r'^download/(?P<object_id>\d+)/$',
                           list_detail.object_detail, download_detail,
                           name='download'),  
                       url(r'^notes/(?P<object_id>\d+)/$',
                           list_detail.object_detail, notes_detail,
                           name='note'),

                       # urls concerning git repositories access
                       url(r'^repo/$', repo_index, name='repo-index'),
                       url(r'^repo/(?P<repo>[\@\w_-]+)/$', repo, name='view-repo'),
                       url(r'^repo/(?P<repo>[\@\w_-]+)/commit/(?P<commit>[\w\d]+)/$', repo_commit, name='repo-commit'),
                       url(r'^repo/(?P<repo>[\@\w_-]+)/commit/(?P<commit>[\w\d]+)/blob/$', repo_blob, name='repo-blob'),
                      
                       # entry key for projects
                       url(r'^(?P<slug>\w+)/$', 
                           list_detail.object_detail,
                           project_detail, name='detail'),

                       )

namespaced = (urlpatterns, 'djpro', 'djpro')

