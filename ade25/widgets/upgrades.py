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
    settings = widget_utils.default_widget_configuration
    api.portal.set_registry_record(
        name='ade25.widgets.widget_settings',
        value=settings
    )


def upgrade_1001(setup):
    setup.runImportStepFromProfile(default_profile, 'registry')
    # Update registry settings
    update_widget_settings()
