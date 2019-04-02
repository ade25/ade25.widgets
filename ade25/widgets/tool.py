# -*- coding: utf-8 -*-
"""Module providing genearal toolset for panel management"""
import datetime
import json
import os
import uuid as uuid_tool

import time

from ade25.base.utils import get_filesystem_template
from ade25.widgets.interfaces import IContentWidgets
from babel.dates import format_datetime
from Products.CMFPlone.utils import safe_unicode
from future.backports import OrderedDict
from future.backports.email.utils import format_datetime
from plone import api
from plone.dexterity.interfaces import IDexterityFTI
from plone.event.utils import pydt
from zope.component import getUtility
from zope.lifecycleevent import modified
from zope.schema import getFieldsInOrder

# from collective.beaker.interfaces import ISession

from ade25.widgets import utils as widget_utils


SESSION_KEY = "Uh53dAfH2JPzI/lIhBvN72RJzZVv6zk5"


class ContentWidgetTool(object):
    """ Utility providing management for content widgets """

    @staticmethod
    def widget_storage(uuid):
        context = api.content.get(UID=uuid)
        return IContentWidgets(context)

    def widget_create(self, uuid, widget_id):
        storage = self.widget_storage(uuid)
        storage.create_widget(widget_id)

    def widget_read(self, uuid, widget_id):
        widget_data = {
            'widget_id': widget_id,
            'data': {
                'state': 'draft',
                'content': dict()
            }
        }
        storage = self.widget_storage(uuid)
        if storage.has_widgets():
            widget_data['data'] = storage.read_widget(widget_id)
        return widget_data

    @property
    def widget_categories(self):
        return widget_utils.content_widget_types_details()

    @property
    def widget_settings(self):
        stored_widget_settings = api.portal.get_registry_record(
            name="ade25.widgets.widget_settings"
        )
        widget_settings = json.loads(stored_widget_settings)
        return widget_settings["items"]

    @staticmethod
    def _widget_information(widget_name, widget_data):
        widget_data['widget'] = widget_name
        return widget_data

    def widget_information(self, widget_category, widget_data):
        settings = self.widget_settings
        info = [
            self._widget_information(widget, settings[widget])
            for widget in widget_data
            if settings[widget]["category"] == widget_category
        ]
        return info

    def section_widgets(self, section_name="main"):
        settings = dict()
        registry_key = "ade25.widgets.content_widgets_{0}".format(section_name)
        widgets_for_section = api.portal.get_registry_record(name=registry_key)
        for category_key, category_name in self.widget_categories.items():
            settings[category_key] = {
                "section_id": category_key,
                "section_title": category_name,
                "items": self.widget_information(
                    category_key,
                    widgets_for_section),
            }
        return settings
