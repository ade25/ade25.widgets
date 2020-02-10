# -*- coding: utf-8 -*-
"""Module providing standalone content panel edit forms"""
from plone.app.textfield import RichText
from plone.app.textfield.widget import RichTextWidget
from plone.autoform.interfaces import IFormFieldProvider
from plone.namedfile import field as named_file
from plone.autoform import directives
from zope import schema
from zope.interface import Interface, provider

from ade25.widgets import MessageFactory as _


@provider(IFormFieldProvider)
class IAde25WidgetImageCover(Interface):
    """ Content widget image cover """

    image = named_file.NamedBlobImage(
        title=_(u"Cover Image"),
        required=True
    )
    image_caption = schema.TextLine(
        title=_(u"Cover Image Copyright Information"),
        required=False
    )


@provider(IFormFieldProvider)
class IAde25WidgetImagePoster(Interface):
    """ Content widget image poster """

    image = named_file.NamedBlobImage(
        title=_(u"Poster Image"),
        required=True
    )
    image_caption = schema.TextLine(
        title=_(u"Poster Image Copyright Information"),
        required=False
    )
    text = RichText(
        title=_(u"Text"),
        required=False,
        allowed_mime_types=('text/html', ),
    )
    directives.widget(
        'text',
        RichTextWidget,
        pattern_options={
            'inline': True
        }
    )