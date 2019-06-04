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
    """ Content annotation storage schema """

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

    def store_widget():
        """
        Store the vote information, store the request hash to ensure
        that the user does not vote twice
        """

    def widget_index():
        """
        Return the widget count for an item
        """

    def has_widgets():
        """
        Return whether widgets are available for this item
        """

    def clear():
        """
        Clear the widgets. Should only be called by admins
        """


alsoProvides(IContentWidgets, IFormFieldProvider)


class IContentWidgetTool(Interface):
    """ Panel data processing

        General tool providing CRUD operations for assigning panel
        layout to content objects
    """

    def create(context):
        """ Create asset assignment data file

        The caller is responsible for passing a valid data dictionary
        containing the necessary details

        Returns JSON object

        @param uuid:        content object UID
        @param data:        predefined initial data dictionary
        """

    def read(context):
        """ Read stored data from object

        Returns a dictionary

        @param uuid:        object UID
        @param key:         (optional) dictionary item key
        """

    def update(context):
        """ Update stored data from object

        Returns a dictionary

        @param uuid:        object UID
        @param key:         (optional) dictionary item key
        @param data:        data dictionary
        """

    def delete(context):
        """ Delete stored data from object

        Returns a dictionary

        @param uuid:        caravan site object UID
        @param key:         (optional) dictionary item key
        """
