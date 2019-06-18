# -*- coding: utf-8 -*-
"""Module providing controlpanels"""
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.autoform import form
from zope import schema
from zope.interface import Interface
from plone.z3cform import layout
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper

from ade25.widgets import utils as widget_utils

from ade25.widgets import MessageFactory as _


class IAde25WidgetsControlPanel(Interface):

    content_widgets_header = schema.List(
        title=_(u"Content Widgets Page Header"),
        description=_(u"Select Content Widgets that should be available "
                      u"for the page header section."),
        value_type=schema.Choice(
            vocabulary='ade25.widgets.vocabularies.AvailableContentWidgets'
        ),
        defaultFactory=widget_utils.default_widget_types_available,
        missing_value=(),
        required=False
    )

    content_widgets_main = schema.List(
        title=_(u"Content Widgets Main Content Area"),
        description=_(u"Select Content Widgets that should be available "
                      u"for the main page content area."),
        value_type=schema.Choice(
            vocabulary='ade25.widgets.vocabularies.AvailableContentWidgets'
        ),
        defaultFactory=widget_utils.default_widget_types_available,
        missing_value=(),
        required=False
    )

    content_widgets_footer = schema.List(
        title=_(u"Content Widgets Page Footer"),
        description=_(u"Select Content Widgets that should be available "
                      u"for the page header section."),
        value_type=schema.Choice(
            vocabulary='ade25.widgets.vocabularies.AvailableContentWidgets'
        ),
        defaultFactory=widget_utils.default_widget_types_available,
        missing_value=(),
        required=False
    )

    widget_settings = schema.Text(
        title=_(u"Widget Settings JSON"),
        description=_(u"Widget configuration registry storing a string "
                      u"representation of a valid JSON settings array"),
        required=False,
        defaultFactory=widget_utils.default_widget_configuration(
            version=1001
        )
    )


class Ade25WidgetsControlPanelForm(RegistryEditForm):
    schema = IAde25WidgetsControlPanel
    schema_prefix = "ade25.widgets"
    label = u'Ade25 Widgets'


Ade25WidgetsSettings = layout.wrap_form(
    Ade25WidgetsControlPanelForm,
    ControlPanelFormWrapper
)
