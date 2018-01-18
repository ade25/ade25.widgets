# -*- coding: utf-8 -*-
"""Module providing controlpanels"""
from plone.app.registry.browser.controlpanel import RegistryEditForm
from zope import schema
from zope.interface import Interface
from plone.z3cform import layout
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper

from ade25.widgets import MessageFactory as _


class IAde25WidgetsControlPanel(Interface):

    available_widgets = schema.Set(
        title=_(u"Activated widgets"),
        description=_(u"Select Content Widgets that should be available "
                      u"for this site. Allows to enable or disable widgets"
                      u"provided by external packages."),
        value_type=schema.Choice(
            vocabulary='ade25.widgets.vocabularies.AvailableContentWidgets'
        ),
        required=False
    )


class Ade25WidgetsControlPanelForm(RegistryEditForm):
    schema = IAde25WidgetsControlPanel
    schema_prefix = "ade25widgets"
    label = u'Ade25 Widgets'


Ade25WidgetsSettings = layout.wrap_form(
    Ade25WidgetsControlPanelForm,
    ControlPanelFormWrapper
)
