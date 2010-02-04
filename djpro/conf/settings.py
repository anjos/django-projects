#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Created by Andre Anjos <andre.dos.anjos@cern.ch>
# Seg 12 Out 2009 11:32:00 CEST 

"""Settings for projects
"""
import os
from django.conf import settings

DJPRO_GIT_BASE_DIRECTORY = getattr(settings, 'DJPRO_GIT_BASE_DIRECTORY',
    os.path.join(os.environ['HOME'], 'git'))

DJPRO_HIGHLIGHT_STYLE = getattr(settings, 'DJPRO_HIGHLIGHT_STYLE', 'default')

# the number of commits to show per page in the commit summary for the repo
DJPRO_COMMITS_PER_PAGE = getattr(settings, 'DJPRO_COMMITS_PER_PAGE', 15)

# the maximum number of tags to show in the commit summary page
DJPRO_MAX_TAGS = getattr(settings, 'DJPRO_MAX_TAGS', 10)
