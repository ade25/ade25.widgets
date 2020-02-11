# -*- coding: utf-8 -*-
# Module providing version specific upgrade steps
import datetime
import json
import logging
import time
import six

from plone import api
from Products.CMFPlone.utils import safe_unicode

from ade25.widgets import utils as widget_utils
from ade25.widgets.config import PKG_WIDGETS

default_profile = 'profile-ade25.widgets:default'
logger = logging.getLogger(__name__)


def update_widget_settings(version=None):
    """Run custom add-on package installation code to modify Plone
       site object and others

    @param version: Requested base configuration version
    """
    settings = widget_utils.default_widget_configuration(version)
    api.portal.set_registry_record(
        name='ade25.widgets.widget_settings',
        value=settings
    )


def register_content_widgets(site):
    """Run custom add-on package installation code to add custom
       site specific content widgets
    @param site: Plone site
    """
    content_widgets = PKG_WIDGETS
    widget_settings = api.portal.get_registry_record(
        name="ade25.widgets.widget_settings"
    )
    stored_widgets = json.loads(widget_settings)
    records = stored_widgets['items']
    for content_widget, widget_data in content_widgets.items():
        if content_widget not in records.keys():
            records[content_widget] = widget_data
    stored_widgets["items"] = records
    stored_widgets["timestamp"] = six.text_type(int(time.time())),
    stored_widgets["updated"] = datetime.datetime.now().isoformat(),
    api.portal.set_registry_record(
        name='ade25.widgets.widget_settings',
        value=safe_unicode(json.dumps(stored_widgets))
    )


def upgrade_1001(setup):
    setup.runImportStepFromProfile(default_profile, 'plone.app.registry')
    # Update registry settings
    update_widget_settings(version=1001)


def upgrade_1002(setup):
    setup.runImportStepFromProfile(default_profile, 'typeinfo')
    portal = api.portal.get()
    # Create a folder for widget asset management if needed
    if 'asset-repository' not in portal:
        api.content.create(
            container=portal,
            type='ade25.widgets.assetsfolder',
            id='asset-repository',
            title=u'Asset Repository')


def upgrade_1003(setup):
    portal = api.portal.get()
    register_content_widgets(portal)


def upgrade_1004(setup):
    portal = api.portal.get()
    setup.runImportStepFromProfile(default_profile, 'plone.app.registry')
    register_content_widgets(portal)
