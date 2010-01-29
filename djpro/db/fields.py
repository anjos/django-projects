#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Created by Andre Anjos <andre.dos.anjos@cern.ch>
# Qui 28 Jan 2010 14:35:36 CET 

"""Implements DB field variations for Git repositories.
"""

from django.db.models.fields import FilePathField
import forms

class GitRepoField(FilePathField):
  """A simple field that inherits from FilePathField and provides GIT support."""

  def __init__(self, *args, **kwargs):
    FilePathField.__init__(self, *args, **kwargs)

  def formfield(self, *args, **kwargs):
    defaults = {'form_class': forms.GitRepoField}
    defaults.update(kwargs)
    return super(GitRepoField, self).formfield(*args, **defaults)
