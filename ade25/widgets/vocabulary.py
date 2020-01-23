# -*- coding: utf-8 -*-
"""Module providing widget vocabularies"""
import json
from binascii import b2a_qp

from plone import api
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from ade25.widgets import MessageFactory as _


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
        settings = json.loads(registry_settings)
        available_widgets = settings['items']
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
