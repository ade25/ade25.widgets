# -*- coding: utf-8 -*-
"""Module providing standalone content panel edit forms"""
from plone.autoform import directives as form
from plone.autoform.interfaces import IFormFieldProvider
from Products.CMFPlone.utils import safe_unicode
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
        default=safe_unicode('20')
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
        default=safe_unicode('20')
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
        default='width-100',
        vocabulary='ade25.widgets.vocabularies.ContentWidgetLayoutOptions'
    )
    display_read_more = schema.Bool(
        title=_(u"Display Read More Link"),
        default=True,
        required=False
    )
    read_more_text = schema.TextLine(
        title=_(u"Read More Text"),
        description=_(u"Enter displayed text for read more element."),
        default=safe_unicode(_(u'Read more')),
        required=False
    )
    form.widget('read_more_layout', klass='js-choices-selector')
    read_more_layout = schema.Choice(
        title=_(u"Read More Layout"),
        description=_(u"Select how the card footer link should be displayed."),
        required=False,
        default='link',
        vocabulary='ade25.widgets.vocabularies.ContentWidgetLayoutOptions'
    )
