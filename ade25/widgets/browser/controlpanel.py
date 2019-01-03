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

    available_widgets = schema.List(
        title=_(u"Activated widgets"),
        description=_(u"Select Content Widgets that should be available "
                      u"for this site. Allows to enable or disable widgets "
                      u"provided by external packages."),
        value_type=schema.Choice(
            vocabulary='ade25.widgets.vocabularies.AvailableContentWidgets'
        ),
        defaultFactory=widget_utils.default_widget_types_available,
        missing_value=(),
        required=False
    )

    widget_types = schema.List(
        title=_(u"Registered Widget Types"),
        description=_(u"Widget types registered for this site. Add ons are "
                      u"required to provide a setup step that adds specific "
                      u"widgets to this list."),
        value_type=schema.TextLine(
            title=_(u"Widget type"),
        ),
        defaultFactory=widget_utils.default_widget_types,
        missing_value=(),
        required=False
    )

    widget_settings = schema.Text(
        title=_(u"Widget Settings JSON"),
        description=_(u"Widget configuration registry storing a string "
                      u"representation of a valid JSON settings array"),
        required=False,
        defaultFactory=widget_utils.default_widget_configuration
    )


class Ade25WidgetsControlPanelForm(RegistryEditForm):
    schema = IAde25WidgetsControlPanel
    schema_prefix = "ade25.widgets"
    label = u'Ade25 Widgets'


Ade25WidgetsSettings = layout.wrap_form(
    Ade25WidgetsControlPanelForm,
    ControlPanelFormWrapper
)
