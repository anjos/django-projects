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

project_list = { 'queryset': Project.objects.all(),
                 'template_name': 'djpro/list.html',
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

  # a PyPI-like index for easy-install and pip
  url(r'^pypi/$', pypi_index, name='pypi-index'), 
  url(r'^pypi/simple/$', pypi_index, 
   {'template_name': 'djpro/pypi_simple_index.html'},
   name='pypi-simple-index'), 
  url(r'^pypi/simple/(?P<slug>\w+)/$', pypi_package,
   {'template_name': 'djpro/pypi_simple_package.html'},
   name='pypi-simple-package'),
  url(r'^pypi/(?P<slug>\w+)/$', pypi_package,
   name='pypi-package'), 
  url(r'^pypi/(?P<slug>\w+)/(?P<version>[\d\.]+)/$', 
   pypi_package, name='pypi-package-version'), 

  # access to the git repositories
  #url(r'^(?P<slug>\w+)/repo', repo_detail, name='view-repo'),
  #url(r'^(?P<slug>\w+)/repo/commit/(?P<commit>[\w\d]+)/$', repo_commit, name='view-commit'),
  #url(r'^(?P<slug>\w+)/repo/diff/(?P<commit>[\w\d]+)/$', repo_diff, name='view-diff'),
  #url(r'^(?P<slug>\w+)/repo/blob/(?P<commit>[\w\d]+)/$', repo_blob, name='view-blob'),
  #url(r'^(?P<slug>\w+)/repo/raw/(?P<commit>[\w\d]+)/$', repo_raw, name='view-raw'),
  #url(r'^(?P<slug>\w+)/repo/tree/(?P<commit>[\w\d]+)/$', repo_tree, name='view-tree'),
  #url(r'^(?P<slug>\w+)/repo/archive/(?P<commit>[\w\d]+)/$', download_tree, name='download-tree'),
  #url(r'^(?P<slug>\w+)/repo/download/$', download_release, name='download-release'),
  #url(r'^(?P<slug>\w+)/repo/history/(?P<commit>[\w\d]+)/$', repo_history, name='view-history'),

  # urls concerning git repositories access
  url(r'^git/$', git_detail, name='view-repo'),
  url(r'^git/commit/(?P<commit>[\w\d]+)/$', git_commit, name='view-commit'),
  url(r'^git/diff/(?P<commit>[\w\d]+)/$', git_diff, name='view-diff'),
  url(r'^git/blob/(?P<commit>[\w\d]+)/$', git_blob, name='view-blob'),
  url(r'^git/raw/(?P<commit>[\w\d]+)/$', git_raw, name='view-raw'),
  url(r'^git/tree/(?P<commit>[\w\d]+)/$', git_tree, name='view-tree'),
  url(r'^git/archive/(?P<commit>[\w\d]+)/$', git_download_tree, name='download-tree'),
  url(r'^git/download/$', git_download_release, name='download-release'),
  url(r'^git/history/(?P<commit>[\w\d]+)/$', git_history, name='view-history'),

  # entry key for projects
  url(r'^(?P<slug>\w+)/$', project_detail, 
     {'feeds': feeds.values(),
      'template_name': 'djpro/detail.html',
     }, 
     name='view-project'), 

)

namespaced = (urlpatterns, 'djpro', 'djpro')

