# -*- coding: utf-8 -*-
# Module providing version specific upgrade steps
import json

from plone import api

import logging

default_profile = 'profile-ade25.widgets:default'
logger = logging.getLogger(__name__)

from ade25.widgets import utils as widget_utils


def update_widget_settings():
    """Run custom add-on package installation code to modify Plone
       site object and others

    @param site: Plone site
    """
    settings = widget_utils.default_widget_configuration()
    api.portal.set_registry_record(
        name='ade25.widgets.widget_settings',
        value=settings
    )


def upgrade_1001(setup):
    setup.runImportStepFromProfile(default_profile, 'plone.app.registry')
    # Update registry settings
    update_widget_settings()


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
