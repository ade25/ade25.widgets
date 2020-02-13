# -*- coding: utf-8 -*-
"""Module providing custom setup steps"""
import datetime
import json
import logging
import time

import six
from Products.CMFPlone.utils import safe_unicode

from ade25.widgets.config import PKG_WIDGETS
from plone import api
from plone.api.exc import InvalidParameterError

logger = logging.getLogger(__name__)


def register_content_widgets(site):
    """ Run custom add-on package installation code to add custom
       site specific content widgets

    @param site: Plone site
    """
    content_widgets = PKG_WIDGETS
    widget_settings = api.portal.get_registry_record(
        name="ade25.widgets.widget_settings"
    )
    try:
        stored_widgets = json.loads(widget_settings)
    except TypeError:
        stored_widgets = {'items': {}}
    records = stored_widgets['items']
    for content_widget, widget_data in content_widgets.items():
        if content_widget not in records.keys():
            records[content_widget] = widget_data
    stored_widgets["items"] = records
    stored_widgets["timestamp"] = (six.text_type(int(time.time())),)
    stored_widgets["updated"] = (datetime.datetime.now().isoformat(),)
    api.portal.set_registry_record(
        name="ade25.widgets.widget_settings",
        value=safe_unicode(json.dumps(stored_widgets)),
    )


def add_assets_repository(site):
    # Create a folder for widget asset management if needed
    if "asset-repository" not in site:
        api.content.create(
            container=site,
            type="ade25.widgets.assetsfolder",
            id="asset-repository",
            title=u"Asset Repository",
        )
        api.content.transition(obj=site["asset-repository"], transition="publish")


def run_after(context):
    """
    @param context: Products.GenericSetup.context.DirectoryImportContext instance
    """

    portal = api.portal.get()

    register_content_widgets(portal)
    add_assets_repository(portal)
