from django.contrib.syndication.feeds import Feed
from django.utils.feedgenerator import Atom1Feed, Rss201rev2Feed
from django.contrib.sites.models import Site
from djpro.models import Project, Download
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import string_concat  as _cat
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse

site = Site.objects.get_current()

class LatestDownloadsForProject(Feed):
  basename = 'downloads'

  def get_object(self, bits):
    if len(bits) != 1:
      raise ObjectDoesNotExist
    try:
      return Project.objects.get(vc__slug=bits[0])
    except:
      raise ObjectDoesNotExist

  def title(self, obj):
    return _("%s downloads" % obj.name)

  def description(self, obj):
    return _("Downloads available for %(project)s" % \
        {'project': obj.name})

  def link(self, obj):
    return reverse('djpro:detail', args=(obj.vc.slug,))

  title_template = "djpro/feeds/downloads_title.html"
  description_template = "djpro/feeds/downloads_description.html"

  def items(self, obj):
    return obj.download_set.exclude(development=True).order_by('-date')

  def item_link(self, item):
    return item.data.url

  def item_pubdate(self, item):
    return item.date

  def item_enclosure_url(self, item):
    return item.data.url

  def item_enclosure_length(self, item):
    return item.data.size

  item_enclosure_mime_type = 'application/octet-stream'

class LatestDeveloperDownloadsForProject(LatestDownloadsForProject):
  basename = 'developer'

  def title(self, obj):
    return _("%s developer downloads" % obj.name)

  def description(self, obj):
    return _("Developer downloads available for %(project)s" % \
        {'project': obj.name})

  def items(self, obj):
    return obj.download_set.order_by('-date')

class SparkleUpcastFeed(Rss201rev2Feed):
  """Special Sparkle Upcast feed, with all stuff that Sparkle wants to have."""

  def __init__(self, *args, **kwargs):
    super(SparkleUpcastFeed, self).__init__(*args, **kwargs)

  def root_attributes(self):
    attrs = super(SparkleUpcastFeed, self).root_attributes()
    attrs['xmlns:sparkle'] = \
        'http://www.andymatuschak.org/xml-namespaces/sparkle'
    attrs['xmlns:dc'] = 'http://purl.org/dc/elements/1.1/'
    return attrs

  def add_item_elements(self, handler, item):
    """Modifies the feed data, so it looks as we need"""
    super(SparkleUpcastFeed, self).add_item_elements(handler, item)
    handler.addQuickElement('sparkle:releaseNotesLink', contents=item['sparkle:releaseNotesLink'])
    handler.addQuickElement('enclosure', attrs=item['_enclosure'])

class SparkleUpdatesForProject(Feed):
  feed_type = SparkleUpcastFeed 
  basename = 'sparkle'

  def get_object(self, bits):
    if len(bits) != 1:
      raise ObjectDoesNotExist
    try:
      return Project.objects.get(vc__slug=bits[0])
    except:
      raise ObjectDoesNotExist

  def title(self, obj):
    return _("%s Changelog" % obj.name)

  def description(self, obj):
    return _("MacOSX Sparkle updates for %(project)s" % \
        {'project':obj.name})

  def link(self, obj):
    return reverse('djpro:detail', args=(obj.vc.slug,))

  title_template = "djpro/feeds/sparkle_title.html"
  description_template = "djpro/feeds/sparkle_description.html"

  def items(self, obj):
    return obj.download_set.exclude(development__exact=True).order_by('-date')

  def item_link(self, item):
    return item.data.url 

  def item_pubdate(self, item):
    return item.date

  def item_extra_kwargs(self, item):
    attrs = {}
    attrs['sparkle:releaseNotesLink'] = \
        'http://%s/project/notes/%d' % (site.domain, item.id)
    attrs['_enclosure'] = {}
    attrs['_enclosure']['url'] = item.data.url 
    attrs['_enclosure']['length'] = str(item.data.size)
    attrs['_enclosure']['type'] = 'application/octet-stream'
    attrs['_enclosure']['sparkle:version'] = item.version 
    if item.dsa_digest:
      attrs['_enclosure']['sparkle:dsaSignature'] = item.dsa_digest
    return attrs

