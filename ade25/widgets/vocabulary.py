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
