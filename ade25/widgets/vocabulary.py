# -*- coding: utf-8 -*-
"""Module providing widget vocabularies"""
from plone import api
from plone.app.vocabularies.terms import safe_simpleterm_from_value
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary


@implementer(IVocabularyFactory)
class AvailableContentWidgetsVocabularyFactory(object):

    def __call__(self, context):
        widgets = self.get_available_widget_records()
        terms = [
            safe_simpleterm_from_value(widget)
            for widget in widgets
        ]
        return SimpleVocabulary(terms)

    @staticmethod
    def get_available_widget_records():
        registry_settings = api.portal.get_registry_record(
            'ade25.widgets.widget_types'
        )
        return registry_settings


AvailableContentWidgetsVocabulary = AvailableContentWidgetsVocabularyFactory()
