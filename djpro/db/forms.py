#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Created by Andre Anjos <andre.dos.anjos@cern.ch>
# Qui 28 Jan 2010 12:14:44 CET 

"""A few variations of form fields needed for GIT repositories
"""

from django.forms.fields import FilePathField 
from .. import utils
import os

class GitRepoField(FilePathField):
  """A form field for git repositories."""

  def __init__(self, path, match=None, recursive=False, required=True,
               widget=None, label=None, initial=None, help_text=None,
               *args, **kwargs):

    self.path, self.match, self.recursive = path, match, recursive
    super(FilePathField, self).__init__(choices=(), required=required,
        widget=widget, label=label, initial=initial, help_text=help_text,
        *args, **kwargs)

    if self.required: self.choices = []
    else: self.choices = [("", "---------")]

    self.choices.extend(utils.get_repo_paths(path, match, recursive))

    self.widget.choices = self.choices

