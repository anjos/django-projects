import settings
from django.conf.urls.defaults import *
from django.contrib import admin
import djpro.urls

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'django.views.generic.simple.direct_to_template',
      {'template': 'base.html'}, name='root'),
    url(r'^p/', djpro.urls.namespaced),
    url(r'^admin/', admin.site.urls),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^jsi18n/(?P<packages>\S+?)/$', 
      'django.views.i18n.javascript_catalog'),
    url(r'^jsi18n/$', 'django.views.i18n.javascript_catalog'),
    url(r'^rosetta/', include('rosetta.urls')),

    # Media serving
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': settings.MEDIA_ROOT,
     'show_indexes': True}
     ), 
    )
