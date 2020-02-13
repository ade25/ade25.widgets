# -*- coding: utf-8 -*-
"""Module providing controlpanels"""
import datetime
import json
import time
import six

from Products.Five import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from ade25.widgets.config import PKG_WIDGETS
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.autoform import form
from plone.autoform import directives as form_directives
from zope import schema
from zope.interface import Interface
from plone.z3cform import layout
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper

from ade25.widgets import utils as widget_utils

from ade25.widgets import MessageFactory as _


class Ade25WidgetsSettings(BrowserView):
    """ Ade25 settings overview """

    def update(self):
        if super(Ade25WidgetsSettings, self).update():
            if 'form.button.setup' in self.request.form:
                self.processSetup()

    def processSetup(self):
        IStatusMessage(self.request).addStatusMessage(
            _(u'Setup initialized.'), 'info')


class IAde25WidgetsControlPanel(Interface):

    content_widgets_header = schema.List(
        title=_(u"Content Widgets Page Header"),
        description=_(u"Select Content Widgets that should be available "
                      u"for the page header section."),
        value_type=schema.Choice(
            vocabulary='ade25.widgets.vocabularies.AvailableContentWidgets'
        ),
        required=False
    )

    content_widgets_main = schema.List(
        title=_(u"Content Widgets Main Content Area"),
        description=_(u"Select Content Widgets that should be available "
                      u"for the main page content area."),
        value_type=schema.Choice(
            vocabulary='ade25.widgets.vocabularies.AvailableContentWidgets'
        ),
        required=False
    )

    content_widgets_footer = schema.List(
        title=_(u"Content Widgets Page Footer"),
        description=_(u"Select Content Widgets that should be available "
                      u"for the page header section."),
        value_type=schema.Choice(
            vocabulary='ade25.widgets.vocabularies.AvailableContentWidgets'
        ),
        required=False
    )

    widget_settings = schema.Text(
        title=_(u"Widget Settings JSON"),
        description=_(u"Widget configuration registry storing a string "
                      u"representation of a valid JSON settings array"),
        required=False,
    )


class Ade25WidgetsControlPanelForm(RegistryEditForm):
    schema = IAde25WidgetsControlPanel
    schema_prefix = "ade25.widgets"
    label = u'Ade25 Widgets'


Ade25WidgetsSettingsBase = layout.wrap_form(
    Ade25WidgetsControlPanelForm,
    ControlPanelFormWrapper
)


class IAde25WidgetsControlPanelWidgets(Interface):

    read_more_icon = schema.TextLine(
        title=_(u"Read More Icon Name"),
        description=_(u"Please enter icon to be used in read more links when "
                      u"a layout with icon is selected. Note: the icon needs to "
                      u"exist in the themes icon sprite for this to work."),
        default=u'chevron',
        required=False
    )

    form_directives.widget('listing_scale', klass='js-choices-selector')
    listing_scale = schema.Choice(
        title=_(u"Content Listing: Image Scale"),
        vocabulary='ade25.widgets.vocabularies.AvailableImageScales',
        default=u'ratio-4:3',
        required=False
    )
    listing_hidden_fields = schema.List(
        title=_(u"Content Listing: Hidden Elements"),
        description=_(u"Please select which elements should be hidden in the "
                      u"widget add and edit forms."),
        value_type=schema.Choice(
            vocabulary='ade25.widgets.vocabularies.ContentWidgetSchemaOptions'
        ),
        default=['text', 'link', ],
        required=False
    )

    form_directives.widget('listing_cards_scale', klass='js-choices-selector')
    listing_cards_scale = schema.Choice(
        title=_(u"Content Listing Cards: Image Scale"),
        vocabulary='ade25.widgets.vocabularies.AvailableImageScales',
        default=u'ratio-4:3',
        required=False
    )
    listing_cards_hidden_fields = schema.List(
        title=_(u"Content Listing Cards: Hidden Elements"),
        description=_(u"Please select which elements should not be available in the "
                      u"widget add and edit forms."),
        value_type=schema.Choice(
            vocabulary='ade25.widgets.vocabularies.ContentWidgetSchemaOptions'
        ),
        default=['text', 'link', ],
        required=False
    )

    form_directives.widget('image_poster_scale', klass='js-choices-selector')
    image_poster_scale = schema.Choice(
        title=_(u"Poster Image: Image Scale"),
        vocabulary='ade25.widgets.vocabularies.AvailableImageScales',
        default=u'ratio-16:9',
        required=False
    )
    image_poster_hidden_fields = schema.List(
        title=_(u"Poster Image: Hidden Elements"),
        description=_(u"Please select which elements should be available in the "
                      u"widget add and edit forms."),
        value_type=schema.Choice(
            vocabulary='ade25.widgets.vocabularies.ContentWidgetSchemaOptions'
        ),
        default=['text', 'link', ],
        required=False
    )


class Ade25WidgetsControlPanelWidgetsForm(RegistryEditForm):
    schema = IAde25WidgetsControlPanelWidgets
    schema_prefix = "ade25.widgets"
    label = u'Ade25 Widgets Settings'


Ade25WidgetsSettingsWidgets = layout.wrap_form(
    Ade25WidgetsControlPanelWidgetsForm,
    ControlPanelFormWrapper
)


class Ade25WidgetsSettingsJSON(BrowserView):
    """ Ade25 settings json export """

    def __call__(self):
        return self.render()

    @staticmethod
    def _widget_configuration():
        content_widgets = PKG_WIDGETS
        return content_widgets

    def render(self):
        msg = _(u"JSON file could not be generated")
        data = {
            'success': False,
            'message': msg
        }
        configuration = self._widget_configuration()
        if configuration:
            data = configuration
        widgets = {
            "items": data,
            "timestamp": six.text_type(int(time.time())),
            "updated": datetime.datetime.now().isoformat()
        }
        self.request.response.setHeader('Content-Type',
                                        'application/json; charset=utf-8')
        return json.dumps(widgets)
