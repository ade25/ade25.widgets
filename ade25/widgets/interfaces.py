# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""
from plone import api
from plone.autoform import directives as form
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import directives
from plone.supermodel import model
from zope import schema

from plone.theme.interfaces import IDefaultPloneLayer
from zope.interface import alsoProvides, Interface


class IAde25WidgetsLayer(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 browser layer."""


# Marker interface for contenttypes that support this behavior
class IContentWidgetSupport(Interface):
    pass


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

    @staticmethod
    def create_widget(request):
        """
        Store the vote information, store the request hash to ensure
        that the user does not vote twice
        """

    @staticmethod
    def widget_index():
        """
        Return the widget count for an item
        """

    @staticmethod
    def has_widgets():
        """
        Return whether widgets are available for this item
        """

    @staticmethod
    def clear():
        """
        Clear the widgets. Should only be called by admins
        """


alsoProvides(IContentWidgets, IFormFieldProvider)
