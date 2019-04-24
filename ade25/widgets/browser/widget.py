# -*- coding: utf-8 -*-
"""Module providing widget editor and view"""
import uuid as uuid_tool
from Acquisition import aq_inner
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.autoform.form import AutoExtensibleForm
from plone.supermodel import model
from plone.z3cform import layout
from plone.z3cform.layout import FormWrapper
from z3c.form import form
from z3c.form import button

from ade25.widgets import MessageFactory as _
from zope import schema
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse


class IContentWidgetSettings(model.Schema):

    custom_class = schema.TextLine(
        title=_(u"Additional CSS Classes"),
        description=_(u"Enter optional css classes that should be applied to "
                      u"the default widget class."),
        required=False
    )
    widget_display = schema.Choice(
        title=_(u"Widget Display"),
        description=_(u"Select responsive behavior for widget"),
        required=False,
        vocabulary='ade25.widgets.vocabularies.ContentWidgetDisplayOptions'
    )


@implementer(IPublishTraverse)
class ContentWidgetForm(AutoExtensibleForm, form.Form):
    """This search form enables you to find users by specifying one or more
    search criteria.
    """

    schema = IContentWidgetSettings
    ignoreContext = True
    css_class = 'o-form o-form--widget'

    label = _(u'Content Widget')
    #template = ViewPageTemplateFile('widget.pt')
    enableCSRFProtection = True
    formErrorsMessage = _(u'There were errors.')

    submitted = False

    def settings(self):
        return self.params

    @property
    def edit_mode(self):
        if self.settings()['widget_mode'] == 'edit':
            return True
        return False

    @property
    def record(self):
        return self.settings()['widget_data']

    def widget_uid(self):
        try:
            widget_id = self.record['id']
        except (KeyError, TypeError):
            widget_id = str(uuid_tool.uuid4())
        return widget_id

    def rendered_widget(self):
        context = aq_inner(self.context)
        if self.settings()['widget_type']:
            view_name = '@@content-widget-{0}'.format(
                self.settings()['widget_type']
            )
            rendered_widget = context.restrictedTraverse(view_name)(
                widget_mode=self.settings()['widget_mode'],
                widget_data=self.settings()['widget_data']
            )
        else:
            view_name = '@@content-widget-base'
            rendered_widget = context.restrictedTraverse(view_name)()
        return rendered_widget

    def applyChanges(self, data):
        # TODO: Implement data storage via widget tool
        pass

    @button.buttonAndHandler(_(u'Update'), name='update')
    def handleApply(self, action):
        request = self.request
        data, errors = self.extractData()

        if errors:
            self.status = self.formErrorsMessage
            return

        if request.get('form.buttons.update', None):
            self.submitted = True
            self.applyChanges(data)
        self.status = "Thank you very much!"


class ContentWidgetFormView(FormWrapper):

    form = ContentWidgetForm

    def __call__(self,
                 widget_type='base',
                 identifier=None,
                 data_set=None,
                 widget_mode='view',
                 **kw):
        self.params = {
            'widget_name': identifier,
            'widget_type': widget_type,
            'widget_mode': widget_mode,
            'widget_data': data_set
        }
        self.update()
        return self.render()

    def settings(self):
        return self.params

    @property
    def edit_mode(self):
        if self.settings()['widget_mode'] == 'edit':
            return True
        return False

    @property
    def record(self):
        return self.settings()['widget_data']

    def widget_uid(self):
        try:
            widget_id = self.record['id']
        except (KeyError, TypeError):
            widget_id = str(uuid_tool.uuid4())
        return widget_id

    def rendered_widget(self):
        context = aq_inner(self.context)
        if self.settings()['widget_type']:
            view_name = '@@content-widget-{0}'.format(
                self.settings()['widget_type']
            )
            rendered_widget = context.restrictedTraverse(view_name)(
                widget_mode=self.settings()['widget_mode'],
                widget_data=self.settings()['widget_data']
            )
        else:
            view_name = '@@content-widget-base'
            rendered_widget = context.restrictedTraverse(view_name)()
        return rendered_widget
