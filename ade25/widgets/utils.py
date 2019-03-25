# -*- coding: utf-8 -*-
"""Module providing utility functions"""
import datetime
import json
import os
import time
import uuid as uuid_tool
from string import Template

from Products.CMFPlone.utils import safe_unicode

from ade25.widgets import MessageFactory as _
from future.backports import OrderedDict
from plone import api


def get_filesystem_template(name, data=dict()):
    template_file = os.path.join(os.path.dirname(__file__), "templates", name)
    template = Template(open(template_file).read())
    composed = template.substitute(data)
    return composed


def default_widget_types_available(widget_types=None):
    if widget_types is None:
        widget_types = []
    return widget_types


def default_widget_types(widget_types=None):
    if widget_types is None:
        widget_types = [
            safe_unicode("Horizontal Line"),
            safe_unicode("Placeholder Widget"),
            safe_unicode("Separator"),
        ]
    return widget_types


def default_widget_configuration(version=None):
    """ Add default widget configuration

    Addon packages are expected to add their custom widget configuration
    requirements to the registry during import and initialization
    """
    if version:
        template_name = "widget-settings-{0}.json".format(version)
    else:
        template_name = "widget-settings.json"
    template = get_filesystem_template(
        template_name,
        data={
            "id": str(uuid_tool.uuid4()),
            "timestamp": str(int(time.time())),
            "created": datetime.datetime.now().isoformat(),
            "updated": datetime.datetime.now().isoformat(),
        },
    )
    try:
        widget_settings = json.loads(template)
        settings = json.dumps(widget_settings)
    except ValueError:
        settings = "{}"
    return safe_unicode(settings)


def content_widget_types():
    types = [
        'general',
        'image',
        'gallery',
        'summary',
        'more'
    ]
    return types


def content_widget_types_details():
    categories = {
        "general": _(u"General"),
        "image": _(u"Image"),
        "gallery": _(u"Gallery"),
        "summary": _(u"Summary"),
        "more": _(u"More")
    }
    return categories
