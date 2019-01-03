# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""
from plone import api
from plone.autoform import directives as form
from plone.supermodel import directives
from plone.supermodel import model
from zope import schema

from plone.theme.interfaces import IDefaultPloneLayer


class IAde25WidgetsLayer(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 browser layer."""


class IContentWidgets(model.Schema):

    if not api.env.debug_mode():
        form.omitted("widgets")
        form.omitted("widget_hashes")

    directives.fieldset(
        "debug",
        label=u"debug",
        fields=("widgets", "widget_hashes")
    )

    widgets = schema.Dict(
        title=u"Widget Data",
        key_type=schema.TextLine(title=u"Widget Identifier"),
        value_type=schema.Int(title=u"Widget Data JSON"),
        required=False,
    )
    widget_hashes = schema.List(
        title=u"Widget Hashes",
        value_type=schema.TextLine(),
        required=False
    )
