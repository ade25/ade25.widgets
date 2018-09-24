# -*- coding: utf-8 -*-
"""Module providing utility functions"""
import datetime
import json
import os
import time
import uuid as uuid_tool
from string import Template

from Products.CMFPlone.utils import safe_unicode


def get_filesystem_template(name, data=dict()):
    template_file = os.path.join(
        os.path.dirname(__file__),
        'templates',
        name
    )
    template = Template(open(template_file).read())
    composed = template.substitute(data)
    return composed


def default_widget_configuration():
    """ Add default widget configuration

    Addon packages are expected to add their custom widget configuration
    requirements to the registry during import and initialization
    """
    template = get_filesystem_template(
        'widget-settings.json',
        data={
            "id": str(uuid_tool.uuid4()),
            "timestamp": str(int(time.time())),
            "created": datetime.datetime.now().isoformat(),
        }
    )
    try:
        widget_settings = json.loads(template)
        settings = json.dumps(widget_settings)
    except ValueError:
        settings = '{}'
    return safe_unicode(settings)
