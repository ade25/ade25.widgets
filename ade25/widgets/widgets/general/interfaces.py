# -*- coding: utf-8 -*-
"""Module providing schema definitions for general widgets"""
from plone.app.textfield import RichText
from plone.autoform.interfaces import IFormFieldProvider
from zope import schema
from zope.interface import Interface, provider

from ade25.panelpage import MessageFactory as _


@provider(IFormFieldProvider)
class IAde25WidgetTextBlock(Interface):
    """ Content widget formatted text """

    text = schema.Text(
        title=_("Text Content"),
        required=False
    )


@provider(IFormFieldProvider)
class IAde25WidgetTextFormatted(Interface):
    """ Content widget formatted text """

    text = RichText(
        title=_(u"Text"),
        required=False
    )