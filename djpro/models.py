from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.utils.translation import string_concat  as _cat
from django.core.urlresolvers import reverse
import os, datetime

class BaseProject(models.Model):
  """Describes a software project.
  
  A few conventions must be noted:
  * The project sources must be hosted on a accessible git repository
  * The short description is taken from <gitdir>/.git/description, if one 
    is found.
  """
  
  name = models.CharField(_(u'Project name'), max_length=128, help_text=_(u'Insert a short, meaningful unique name for your project.'))

  vc = models.ForeignKey('djit.Repository', help_text=_(u'Choose the repository to do version-control on this project.'), null=False, unique=True) 

  changed = models.DateTimeField(_(u'Last update'), auto_now_add=True, help_text=_(u'The date and time of the last update of this project description.'))

class Project(BaseProject):
  """A Simple project with normal downloads, icons and screenshots."""

  def _updated(self):
    """Returns the last modification time for this project.
    
    Returns the last time a download was added to this project or the last
    time a modification was done to its description (the most recent of the two
    is returned."""

    # get the last git commit date, in naive format (no timezone), 
    # but pay attention to the conversion!
    if self.vc:
      latest = self.vc.updated.replace(tzinfo=None)
    else:
      latest = datetime.datetime.min

    # check the update time
    if self.changed > latest: latest = self.changed

    # check downloads
    downloads = [k.date for k in self.download_set.all()]
    if downloads: latest = max(downloads)

    # check screenshots
    screenshots = [k.date for k in self.screenshot_set.all()]
    if screenshots and max(screenshots) > latest: latest = max(screenshots)

    # check icons
    icons = [k.date for k in self.icon_set.all()]
    if icons and max(icons) > latest: latest = max(icons)

    return latest 

  updated = property(_updated)

  def _public_downloads(self):
    return self.download_set.filter(development=False)
  public_downloads = property(_public_downloads)

  def __unicode__(self):
    return ugettext(u'Project \'%(name)s\'' % {'name': self.name})

class MacProject(Project):
  """A Project that can be installed with sparkle and runs on OSX."""
  
  dsa_pubkey = models.TextField(_(u'DSA project key'), null=True, blank=True, help_text=_('If you have one, insert here the <b>public</b> DSA key for this project.')) 

  class Meta:
    verbose_name = _('mac project')
    verbose_name_plural = _('mac projects')
  
class PythonProject(Project):
  """A Project that can be installed with setuptools."""

  class Meta:
    verbose_name = _('python project')
    verbose_name_plural = _('python projects')

# Place project files in a specific project directory 
def upload_path(instance, filename):
  path = os.path.join('projects', instance.project.vc.slug)
  if isinstance(instance, Download): path = os.path.join(path, 'downloads')
  if isinstance(instance, Screenshot): path = os.path.join(path, 'screenshots')
  if isinstance(instance, Icon): path = os.path.join(path, 'icons')
  path = os.path.join(path, datetime.date.today().strftime('%Y-%m-%d'))
  return os.path.join(path, os.path.basename(filename).lower())

class Download(models.Model):
  """Describes a download associated with a project."""

  name = models.CharField(_('Name'), max_length=256, help_text=_('The name of the file. Can contain spaces and other special characters'))

  description = models.TextField(_('Description'), null=True, blank=True, help_text=_('Explain what this file is - be verbose!'))

  summary=models.CharField(_('Short description'), max_length=1024, blank=False, null=False, help_text=_('Enter an (obligatory) short description of this download'))

  data = models.FileField(_('Download'), upload_to=upload_path, help_text=_('Specify here the file that will be uploaded.'))

  date = models.DateTimeField(_('Upload date'), auto_now_add=True, help_text=_('Sets the insertion date of this file'))

  version=models.CharField(_('Version'), max_length=128, blank=False, null=False, help_text=_('Enter an alpha-numeric version identifier for this download (e.g. 0.3.7, or r245). Please note we may try to find the location of this tag inside your repository, so matching version names and tags is a good idea.'))

  development=models.BooleanField(_('Developer release'), default=True, help_text=_('Mark this box if you want this download to be only visible to developers subscribing a special feed.'))

  project=models.ForeignKey(Project, null=False, blank=False)

  def __unicode__(self):
    return ugettext(u'Download %(version)s from %(project)s' % \
        {'version': self.version, 'project': self.project.name})

  # make it translatable
  class Meta:
    verbose_name = _('download')
    verbose_name_plural = _('downloads')
    unique_together = ('project', 'version')

class MacDownload(Download):
  """Describes a download associated with a project."""

  dsa_digest=models.CharField(_('DSA Digest'), max_length=256, blank=True, null=True, help_text=_('Insert the DSA digest for this download. It will be used to check the file sanity and authenticate it'))

  # make it translatable
  class Meta:
    verbose_name = _('mac download')
    verbose_name_plural = _('mac downloads')

class Screenshot(models.Model):
  """Describes a screenshot of your project"""

  name = models.CharField(_('Name'), max_length=256, help_text=_('The name of the file. Can contain spaces and other special characters'))

  data = models.ImageField(_('Screenshot'), upload_to=upload_path, help_text=_('Specify here the file that will be uploaded.'))

  date = models.DateTimeField(_('Upload date'), auto_now_add=True, help_text=_('Sets the insertion date of this file'))

  project=models.ForeignKey(Project, null=False, blank=False)

  def __unicode__(self):
    return ugettext(u'Screenshot %(name)s from %(project)s' % \
        {'name': self.name, 'project': self.project.name})

  # make it translatable
  class Meta:
    verbose_name = _('screenshot')
    verbose_name_plural = _('screenshots')

class Icon(models.Model):
  """Describes an icon file associated with a project"""

  data = models.ImageField(_('Icon'), upload_to=upload_path, help_text=_('Specify here the file that will be uploaded.'))

  date = models.DateTimeField(_('Upload date'), auto_now_add=True, help_text=_('Sets the insertion date of this file'))

  project=models.ForeignKey(Project, null=False, blank=False)

  def __unicode__(self):
    return ugettext(u'Icon from %(project)s' % {'project': self.project.name})

  # make it translatable
  class Meta:
    verbose_name = _('icon')
    verbose_name_plural = _('icons')
