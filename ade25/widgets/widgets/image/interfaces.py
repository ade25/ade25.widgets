# -*- coding: utf-8 -*-
"""Module providing standalone content panel edit forms"""
from plone import api
from plone.app.textfield import RichText
from plone.app.textfield.widget import RichTextWidget
from plone.app.vocabularies.catalog import CatalogSource
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform.interfaces import IFormFieldProvider
from plone.namedfile import field as named_file
from plone.autoform import directives
from z3c.relationfield import RelationChoice
from zope import schema
from zope.component import queryUtility
from zope.interface import Interface, provider

from ade25.widgets import MessageFactory as _
from zope.schema.interfaces import IVocabularyFactory


def asset_repository_path(context=None):
    portal = api.portal.get()
    folder = portal['asset-repository']
    return '/'.join(folder.getPhysicalPath())


def assets_vocabulary(context=None):
    portal = api.portal.get()
    factory = queryUtility(IVocabularyFactory, 'plone.app.vocabularies.Catalog')
    vocabulary = factory(portal)
    return vocabulary


@provider(IFormFieldProvider)
class IAde25WidgetImageCover(Interface):
    """ Content widget image cover """

    image = named_file.NamedBlobImage(
        title=_(u"Cover Image"),
        required=False
    )
    image_related = RelationChoice(
        title=_(u"Cover Image Select"),
        description=_(u"Select existing image in the asset repository"),
        required=False,
        default=None,
        vocabulary='ade25.widgets.vocabularies.ContentWidgetAssets'
    )

    directives.widget(
        'image_related',
        RelatedItemsFieldWidget,
        pattern_options={
            'recentlyUsed': False,
            'basePath':  asset_repository_path(),
            'path':  asset_repository_path(),
            'mode': 'auto',
            'favorites': [],
            'folderTypes': ['Folder', 'ade25.widgets.assetsfolder', ],
            'selectableTypes': ['Image'],
        }
    )

    image_alt = schema.TextLine(
        title=_(u"Cover Image Alt Text"),
        required=False
    )

    image_title = schema.TextLine(
        title=_(u"Cover Image Title Text"),
        required=False
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
    #text = RichText(
    #    title=_(u"Text"),
    #    required=False,
    #    allowed_mime_types=('text/html', ),
    #)
