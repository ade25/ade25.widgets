# -*- coding: utf-8 -*-
"""Module providing asset folder contents"""
from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer


class IAssetsFolder(model.Schema):
    """Collection of static assets

    A folder providing a global asset repository acting as an image and
    potentially file storage for content widgets
    """


@implementer(IAssetsFolder)
class AssetsFolder(Container):
    pass
