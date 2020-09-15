# -*- coding: utf-8 -*-
"""Module providing widget vocabularies"""
import json
from binascii import b2a_qp

from plone import api
from plone.app.layout.navigation.root import getNavigationRootObject
from plone.app.vocabularies.catalog import CatalogVocabulary
from plone.app.vocabularies.utils import parseQueryString
from zope.component.hooks import getSite
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from ade25.widgets import MessageFactory as _


@implementer(IVocabularyFactory)
class ContentWidgetSectionsVocabularyFactory(object):

    def __call__(self, context):
        widgets = self.get_display_options()
        terms = [
            self.generate_simple_term(widget_key, widget_term)
            for widget_key, widget_term in widgets.items()
        ]
        return SimpleVocabulary(terms)

    @staticmethod
    def generate_simple_term(widget, widget_term):
        term = SimpleTerm(
            value=widget,
            token=b2a_qp(widget.encode('utf-8')),
            title=_(widget_term)
        )
        return term

    @staticmethod
    def get_display_options():
        display_options = {
            'content-widgets-page-header': _(u'Content Widgets Page Header'),
            'content-widgets-page-main': _(u'Content Widgets Main Content Area'),
            'content-widgets-page-footer': _(u'Content Widgets Page Footer')
        }
        return display_options


ContentWidgetSectionsVocabulary = ContentWidgetSectionsVocabularyFactory()


@implementer(IVocabularyFactory)
class AvailableContentWidgetsVocabularyFactory(object):

    def __call__(self, context):
        widgets = self.get_available_widget_records()
        terms = [
            self.generate_simple_term(widget_key, widget_data)
            for widget_key, widget_data in widgets.items()
        ]
        return SimpleVocabulary(terms)

    @staticmethod
    def generate_simple_term(widget, widget_data):
        term = SimpleTerm(
            value=widget,
            token=b2a_qp(widget.encode('utf-8')),
            title=_(widget_data['title'])
        )
        return term

    @staticmethod
    def get_available_widget_records():
        registry_settings = api.portal.get_registry_record(
            'ade25.widgets.widget_settings'
        )
        try:
            settings = json.loads(registry_settings)
            available_widgets = settings['items']
        except TypeError:
            available_widgets = dict()
        return available_widgets


AvailableContentWidgetsVocabulary = AvailableContentWidgetsVocabularyFactory()


@implementer(IVocabularyFactory)
class ContentWidgetDisplayVocabularyFactory(object):

    def __call__(self, context):
        widgets = self.get_display_options()
        terms = [
            self.generate_simple_term(widget_key, widget_term)
            for widget_key, widget_term in widgets.items()
        ]
        return SimpleVocabulary(terms)

    @staticmethod
    def generate_simple_term(widget, widget_term):
        term = SimpleTerm(
            value=widget,
            token=b2a_qp(widget.encode('utf-8')),
            title=_(widget_term)
        )
        return term

    @staticmethod
    def get_display_options():
        display_options = {
            'u-display--none': _(u'Hidden'),
            'u-display--block|u-display-sm--none': _(u'Hidden from 576px'),
            'u-display--block|u-display-md--none': _(u'Hidden from 768px'),
            'u-display--block|u-display-lg--none': _(u'Hidden from 992px'),
            'u-display--block|u-display-xl--none': _(u'Hidden from 1200px'),
            'u-display--block|u-display-xxl--none': _(u'Hidden from 1400px'),
            'u-display--block|u-display-xxxl--none': _(u'Hidden from 1600px'),
            'u-display--block': _(u'Visible'),
            'u-display--none|u-display-sm--block': _(u'Visible from 576px'),
            'u-display--none|u-display-md--block': _(u'Visible from 768px'),
            'u-display--none|u-display-lg--block': _(u'Visible from 992px'),
            'u-display--none|u-display-xl--block': _(u'Visible from 1200px'),
            'u-display--none|u-display-xxl--block': _(u'Visible from 1400px'),
            'u-display--none|u-display-xxxl--block': _(u'Visible from 1600px'),
        }
        return display_options


ContentWidgetDisplayVocabulary = ContentWidgetDisplayVocabularyFactory()


@implementer(IVocabularyFactory)
class ContentWidgetLayoutVocabularyFactory(object):

    def __call__(self, context):
        widgets = self.get_display_options()
        terms = [
            self.generate_simple_term(widget_key, widget_term)
            for widget_key, widget_term in widgets.items()
        ]
        return SimpleVocabulary(terms)

    @staticmethod
    def generate_simple_term(widget, widget_term):
        term = SimpleTerm(
            value=widget,
            token=b2a_qp(widget.encode('utf-8')),
            title=_(widget_term)
        )
        return term

    @staticmethod
    def get_display_options():
        display_options = {
            'width-50': _(u'2 card per row'),
            'width-33': _(u'3 cards per row (default)'),
            'width-25': _(u'4 cards per row')
        }
        return display_options


ContentWidgetLayoutVocabulary = ContentWidgetLayoutVocabularyFactory()


@implementer(IVocabularyFactory)
class ContentWidgetReadMoreLayoutVocabularyFactory(object):

    def __call__(self, context):
        widgets = self.get_display_options()
        terms = [
            self.generate_simple_term(widget_key, widget_term)
            for widget_key, widget_term in widgets.items()
        ]
        return SimpleVocabulary(terms)

    @staticmethod
    def generate_simple_term(widget, widget_term):
        term = SimpleTerm(
            value=widget,
            token=b2a_qp(widget.encode('utf-8')),
            title=_(widget_term)
        )
        return term

    @staticmethod
    def get_display_options():
        display_options = {
            "link": _(u'Plain Link'),
            "link-icon": _(u'Link with icon after the link text'),
            "link-icon-prefix": _(u'Link with icon before the link text'),
            "icon": _(u'Icon only'),
            "button": _(u'Button'),
            "button-icon": _(u'Button with icon after the link text'),
            "button-icon-prefix": _(u'Button with icon before the link text'),
        }
        return display_options


ContentWidgetReadMoreLayoutVocabulary = ContentWidgetReadMoreLayoutVocabularyFactory()


@implementer(IVocabularyFactory)
class AvailableImageScalesVocabularyFactory(object):

    def __call__(self, context):
        widgets = self.get_display_options()
        terms = [
            self.generate_simple_term(widget_key, widget_term)
            for widget_key, widget_term in widgets.items()
        ]
        return SimpleVocabulary(terms)

    @staticmethod
    def generate_simple_term(widget, widget_term):
        term = SimpleTerm(
            value=widget,
            token=b2a_qp(widget.encode('utf-8')),
            title=_(widget_term)
        )
        return term

    @staticmethod
    def get_display_options():
        display_options = {}
        registry_settings = api.portal.get_registry_record(
            'ade25.base.responsive_image_scales'
        )
        for image_scale in registry_settings:
            scale_information = json.loads(image_scale)
            scale_info = next(iter(scale_information.keys()))
            display_options[scale_info] = scale_info.capitalize()
        return display_options


AvailableImageScalesVocabulary = AvailableImageScalesVocabularyFactory()


@implementer(IVocabularyFactory)
class ContentWidgetSchemaVocabularyFactory(object):

    def __call__(self, context):
        widgets = self.get_display_options()
        terms = [
            self.generate_simple_term(widget_key, widget_term)
            for widget_key, widget_term in widgets.items()
        ]
        return SimpleVocabulary(terms)

    @staticmethod
    def generate_simple_term(widget, widget_term):
        term = SimpleTerm(
            value=widget,
            token=b2a_qp(widget.encode('utf-8')),
            title=_(widget_term)
        )
        return term

    @staticmethod
    def get_display_options():
        display_options = {
            'headline': _(u'Headline'),
            'abstract': _(u'Abstract'),
            'text': _(u'Formatted Text'),
            'link': _(u"Link")
        }
        return display_options


ContentWidgetSchemaVocabulary = ContentWidgetSchemaVocabularyFactory()


@implementer(IVocabularyFactory)
class WidgetAssetsCatalogVocabularyFactory(object):

    def __call__(self, context, query=None):
        parsed = {}
        if query:
            parsed = parseQueryString(context, query['criteria'])
            if 'sort_on' in query:
                parsed['sort_on'] = query['sort_on']
            if 'sort_order' in query:
                parsed['sort_order'] = str(query['sort_order'])

        # If no path is specified check if we are in a sub-site and use that
        # as the path root for catalog searches
        if 'path' not in parsed:
            site = getSite()
            nav_root = api.portal.get()
            site_path = site.getPhysicalPath()
            if nav_root and nav_root.getPhysicalPath() != site_path:
                parsed['path'] = {
                    'query': '/'.join(nav_root.getPhysicalPath()),
                    'depth': -1
                }
        return CatalogVocabulary.fromItems(parsed, context)


ContentWidgetAssetsVocabulary = WidgetAssetsCatalogVocabularyFactory()
