# -*- coding: utf-8 -*-
"""Module providing widget editor and view"""
import uuid as uuid_tool
from Acquisition import aq_inner
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.autoform.form import AutoExtensibleForm
from plone.supermodel import model
from plone.z3cform import layout
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
        request = self.request
        request_parameter = {
            'widget_name': getattr(request, 'identifier', None),
            'widget_type': getattr(request, 'widget_type', 'base'),
            'widget_mode': getattr(request, 'widget_mode', 'view'),
            'widget_data': getattr(request, 'widget_date', dict())
        }
        return request_parameter

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


ContentWidgetFormView = layout.wrap_form(
    ContentWidgetForm
)


class ContentWidgetView(BrowserView):
    """ Default widget view

    Renders the provided template and view by the widget in question
    """
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
        return self.render()

    def render(self):
        return self.index()

    @property
    def edit_mode(self):
        if self.params['widget_mode'] == 'edit':
            return True
        return False

    @property
    def record(self):
        return self.params['widget_data']

    def widget_uid(self):
        try:
            widget_id = self.record['id']
        except (KeyError, TypeError):
            widget_id = str(uuid_tool.uuid4())
        return widget_id

    def rendered_widget(self):
        context = aq_inner(self.context)
        if self.params['widget_type']:
            view_name = '@@content-widget-{0}'.format(
                self.params['widget_type']
            )
            rendered_widget = context.restrictedTraverse(view_name)(
                widget_mode=self.params['widget_mode'],
                widget_data=self.params['widget_data']
            )
        else:
            view_name = '@@content-widget-base'
            rendered_widget = context.restrictedTraverse(view_name)()
        return rendered_widget

    def widget_form(self):
        """ Create a form instance.

        @return: z3c.form wrapped for Plone 3 view
        """

        context = aq_inner(self.context)
        # Create a compact version of the contact form
        # (not all fields visible)
        widget_form = ContentWidgetFormView(context, self.request)

        # Wrap a form in Plone view
        view = ContentWidgetView(context, self.request)
        view = view.__of__(context)  # Make sure acquisition chain is respected
        view.form_instance = widget_form
        return view

