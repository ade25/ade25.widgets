# -*- coding: utf-8 -*-
"""Module providing standalone content panel edit forms"""
from plone.autoform.interfaces import IFormFieldProvider
from plone.autoform import directives as form
from zope import schema
from zope.interface import Interface, provider

from ade25.widgets import MessageFactory as _


@provider(IFormFieldProvider)
class IAde25WidgetListing(Interface):
    """ Content widget listing snippets """

    title = schema.TextLine(
        title=_(u"Headline"),
        description=_(u"Enter optional headline to display above the listing."),
        required=False
    )
    display_limit = schema.TextLine(
        title=_(u"Display Limit"),
        description=_(u"Select maximum number of snippets to display. Leave "
                      u"empty when the widget should list all content items."),
        required=False,
        default='20'
    )
    display_batch = schema.Bool(
        title=_(u"Display Pagination"),
        description=_(u"When selected the listing will show the contents divided "
                      u"into pages and display batch navigation. The configured "
                      u"display limit will refer to the maximum number of items"
                      u" per page and the widget will always show all content."),
        default=False,
        required=False
    )
    display_images = schema.Bool(
        title=_(u"Cover Images"),
        description=_(u"Display lead images in content cards."),
        default=True,
        required=False
    )


@provider(IFormFieldProvider)
class IAde25WidgetListingCards(Interface):
    """ Content widget listing cards """

    title = schema.TextLine(
        title=_(u"Headline"),
        description=_(u"Enter optional headline to display above the listing."),
        required=False
    )
    display_limit = schema.TextLine(
        title=_(u"Display Limit"),
        description=_(u"Select maximum number of snippets to display. Leave "
                      u"empty when the widget should list all content items."),
        required=False,
        default='20'
    )
    display_batch = schema.Bool(
        title=_(u"Display Pagination"),
        description=_(u"When selected the listing will show the contents divided "
                      u"into pages and display batch navigation. The configured "
                      u"display limit will refer to the maximum number of items"
                      u" per page and the widget will always show all content."),
        default=False,
        required=False
    )
    display_images = schema.Bool(
        title=_(u"Cover Images"),
        description=_(u"Display lead images in content snippets."),
        default=True,
        required=False
    )
    form.widget('display_columns', klass='js-choices-selector')
    display_columns = schema.Choice(
        title=_(u"Listing Layout"),
        description=_(u"Select the number of cards that should be displayed "
                      u"per column if the screen size allows for horizontal "
                      u"alignment."),
        required=False,
        default='3',
        vocabulary='ade25.widgets.vocabularies.ContentWidgetLayoutOptions'
    )
