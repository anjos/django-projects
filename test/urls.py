import os 
import settings
from django.conf.urls.defaults import *
from django.contrib import admin
from django.views.generic.simple import redirect_to
import djit.urls

exec 'from %s.urls import namespaced as test_urls' % settings.PROJECT

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', redirect_to, {'url': '/p'}),
    url(r'^p/', test_urls),
    url(r'^git/', djit.urls.namespaced),
    url(r'^admin/', admin.site.urls),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^jsi18n/(?P<packages>\S+?)/$', 
      'django.views.i18n.javascript_catalog'),
    url(r'^jsi18n/$', 'django.views.i18n.javascript_catalog'),
    url(r'^rosetta/', include('rosetta.urls')),

    # Media serving
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': settings.MEDIA_ROOT,
     'show_indexes': True},
     name='media'), 
    )
