# -*- coding: utf-8 -*-
"""Module providing schema definitions for general widgets"""
from plone.app.textfield import RichText
from plone.autoform.interfaces import IFormFieldProvider
from zope import schema
from zope.interface import Interface, provider

from ade25.widgets import MessageFactory as _


@provider(IFormFieldProvider)
class IAde25WidgetSeparator(Interface):
    """ Content widget separator """


@provider(IFormFieldProvider)
class IAde25WidgetHorizontalLine(Interface):
    """ Content widget horizontal line """


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


@provider(IFormFieldProvider)
class IAde25WidgetTextHtml(Interface):
    """ Content widget html text """

    text = schema.Text(
        title=_("HTML Content"),
        required=False
    )


@provider(IFormFieldProvider)
class IAde25WidgetPageHeader(Interface):
    """ Content Widget to display page header """

    headline = schema.TextLine(
        title=u"Page Headline",
        description=_(u"Please enter the main page headline."),
        required=False,
    )

    abstract = schema.Text(
        title=u"Page Abstract",
        description=_(u"Use the abstract to provide a short description of ."
                      u"the page content."),
        required=False,
    )
