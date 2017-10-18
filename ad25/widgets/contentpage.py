# -*- coding: utf-8 -*-
"""Module providing ContentPage content type functionality"""

from plone.dexterity.content import Container
from plone.directives import form
from plone.namedfile.interfaces import IImageScaleTraversable
from zope.interface import implementer

from ad25.sitecontent import MessageFactory as _


class IContentPage(form.Schema, IImageScaleTraversable):
    """
    A folderish page
    """


@implementer(IContentPage)
class ContentPage(Container):
    pass
