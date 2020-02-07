# -*- coding: utf-8 -*-
"""Module providing standalone content panel edit forms"""
from plone.app.textfield import RichText
from plone.app.z3cform.widget import LinkFieldWidget
from plone.autoform import directives as form
from plone.autoform.interfaces import IFormFieldProvider
from plone.namedfile import field as named_file
from zope import schema
from zope.interface import Interface, provider

from ade25.panelpage import MessageFactory as _


@provider(IFormFieldProvider)
class IAde25WidgetSlider(Interface):
    """ Content Widget Slider """
    pass


@provider(IFormFieldProvider)
class IAde25WidgetSliderItem(Interface):
    """ Slide """

    image = named_file.NamedBlobImage(
        title=_(u"Slide Image"),
        required=True
    )
    image_caption = schema.TextLine(
        title=_(u"Image Copyright Information"),
        required=False
    )

    headline = schema.TextLine(
        title=_(u"Headline"),
        required=False
    )

    text = RichText(
        title=_(u"Text"),
        required=False
    )

    form.widget(link=LinkFieldWidget)
    link = schema.TextLine(
        title=_(u"Link"),
        description=_(u"Optional internal or external link that will be "
                      u"used as redirection target when section is accessed."
                      u"Logged in users will see the target link instead."),
        required=False,
    )
