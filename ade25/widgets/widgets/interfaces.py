# -*- coding: utf-8 -*-
"""Module providing widget settings"""
from plone.app.textfield import RichText
from plone.autoform import directives as form
from plone.autoform.interfaces import IFormFieldProvider
from Products.CMFPlone.utils import safe_unicode
from zope import schema
from zope.interface import Interface, provider
from plone.app.z3cform.widget import LinkFieldWidget

from ade25.widgets import MessageFactory as _


@provider(IFormFieldProvider)
class IAde25WidgetPartialReadMore(Interface):
    """ Content widget listing snippets """
    display_read_more = schema.Bool(
        title=_(u"Display Read More Link"),
        default=True,
        required=False
    )
    read_more_text = schema.TextLine(
        title=_(u"Read More Text"),
        description=_(u"Enter displayed text for read more element."),
        default=_(u'Read more'),
        required=False
    )
    form.widget('read_more_layout', klass='js-choices-selector')
    read_more_layout = schema.Choice(
        title=_(u"Read More Layout"),
        description=_(u"Select how the card footer link should be displayed."),
        required=False,
        default='link',
        vocabulary='ade25.widgets.vocabularies.ContentWidgetReadMeLayoutOptions'
    )


@provider(IFormFieldProvider)
class IAde25WidgetPartialContentMain(Interface):
    """ Content widget main elements """

    headline = schema.TextLine(
        title=_(u"Headline"),
        required=False
    )

    abstract = schema.Text(
        title=_(u"Abstract"),
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