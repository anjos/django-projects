#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Created by Andre Anjos <andre.dos.anjos@cern.ch>
# Thu 24 Jul 15:36:10 2008 

from django.contrib import admin
from djpro.models import * 
from django.utils.translation import ugettext_lazy as _

def count_all_downloads(instance):
  return instance.download_set.count()
count_all_downloads.short_description = _(u'Downloads')

def count_downloads(instance):
  return instance.download_set.filter(development=True).count()
count_downloads.short_description = _(u'Public downloads')

class ProjectAdmin(admin.ModelAdmin):
  list_display = ('name', Project._updated, 'vc', count_downloads, count_all_downloads)
  list_filter = ['changed', 'name']
  list_per_page = 10
  ordering = ['-changed']
  search_fields = ['name', 'vc']
  date_hierarchy = 'changed'
    
admin.site.register(PythonProject, ProjectAdmin)
admin.site.register(MacProject, ProjectAdmin)

class DownloadAdmin(admin.ModelAdmin):
  list_display = ('name', 'date', 'development', 'project')
  list_filter = ['name', 'date', 'project']
  search_fields = ['name', 'date', 'project']
  date_hierarchy = 'date'
  list_per_page = 10
  ordering = ['-date']

class ScreenshotAdmin(admin.ModelAdmin):
  list_display = ('name', 'date', 'project')
  list_filter = ['name', 'date', 'project']
  search_fields = ['name', 'date', 'project']
  date_hierarchy = 'date'
  list_per_page = 10
  ordering = ['-date']

class IconAdmin(admin.ModelAdmin):
  list_display = ('name', 'date', 'project')
  list_filter = ['name', 'date', 'project']
  search_fields = ['name', 'date', 'project']
  date_hierarchy = 'date'
  list_per_page = 10
  ordering = ['-date']

admin.site.register(Download, DownloadAdmin)
admin.site.register(Screenshot, ScreenshotAdmin)
admin.site.register(Icon)
