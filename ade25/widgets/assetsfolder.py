# -*- coding: utf-8 -*-
"""Module providing asset folder contents"""
from plone.directives import dexterity, form
from zope.interface import implementer


class IAssetsFolder(form.Schema):
    """Collection of static assets

    A folder providing a global asset repository acting as an image and
    potentially file storage for content widgets
    """


@implementer(IAssetsFolder)
class AssetsFolder(dexterity.Container):
    pass
