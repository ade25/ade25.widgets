# -*- coding: utf-8 -*-
"""Module providing widget editor and view"""
import hashlib
import uuid
import uuid as uuid_tool

from Acquisition import aq_inner
from ade25.panelpage.interfaces import IPanelEditor
from plone import api
from plone.autoform.form import AutoExtensibleForm
from plone.namedfile.interfaces import INamedBlobImage
from plone.supermodel import model
from plone.z3cform.layout import FormWrapper
from z3c.form import button
from z3c.form import form
from zope import schema
from zope.component import getUtility
from zope.dottedname.resolve import resolve
from zope.interface import implementer
from zope.lifecycleevent import modified
from zope.publisher.interfaces import IPublishTraverse


from ade25.widgets.interfaces import IContentWidgetTool, IContentWidgets
from ade25.widgets import MessageFactory as _


class IContentWidgetSettings(model.Schema):

    is_public = schema.Bool(
        title=_(u"Public"),
        description=_(u"Select if this widget should be visible in the view "
                      u"or remain in a draft version."),
        default=True,
        required=False
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

    @property
    def panel_editor(self):
        tool = getUtility(IPanelEditor)
        return tool.get()

    @property
    def additionalSchemata(self):
        context = aq_inner(self.context)
        editor_data = self.panel_editor[context.UID()]
        try:
            schema_interface = resolve(editor_data['widget_settings']['schema'])
            schemata = (schema_interface,)
            return schemata
        except ValueError:
            return ()

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

    @property
    def action(self):
        """ Rewrite HTTP POST action.
#        If the form is rendered embedded on the others pages we
        make sure the form is posted through the same view always,
        instead of making HTTP POST to the page where the form was rendered.
        """
        return self.context.absolute_url() + "/@@content-widget-form"

    @staticmethod
    def prettify_key(entry_key):
        try:
            clean_key = entry_key.split(".")[-1]
            return clean_key
        except IndexError:
            return entry_key

    @staticmethod
    def generate_hash_from_filename(file_name):
        return hashlib.sha1(str(uuid.uuid4()) + file_name).hexdigest()

    def _process_image_asset(self, field_key, field_value):
        portal = api.portal.get()
        asset_repository = portal['asset-repository']
        widget_file = api.content.create(
            container=asset_repository,
            type="Image",
            title="Widget Asset {0}".format(
                self.generate_hash_from_filename(field_value.filename)
            )
        )
        modified(widget_file)
        widget_file.reindexObject(idxs='modified')
        return widget_file.UID()

    def applyChanges(self, data):
        # TODO: Implement data storage via widget tool
        context = aq_inner(self.context)
        editor_data = self.panel_editor[context.UID()]
        storage = IContentWidgets(context)
        widget_content = dict()
        for key, value in data.items():
            entry_key = self.prettify_key(key)
            if INamedBlobImage.providedBy(value):
                # TODO: handle file upload to dedicated asset object
                image_uid = self._process_image_asset(entry_key, value)
                widget_content[entry_key] = image_uid
            else:
                widget_content[entry_key] = value
        storage.store_widget(
            editor_data['widget_id'],
            widget_content,
            self.request
        )
        next_url = '{0}/@@panel-page'.format(context.absolute_url())
        return self.request.response.redirect(next_url)

    @button.buttonAndHandler(_(u'cancel'), name='cancel')
    def handleCancel(self, action):
        context = aq_inner(self.context)
        next_url = '{0}/@@panel-page'.format(context.absolute_url())
        return self.request.response.redirect(next_url)

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

    def updateActions(self):
        super(ContentWidgetForm, self).updateActions()
        self.actions["update"].addClass("c-button--primary")
        self.actions["cancel"].addClass("c-button--default")


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

    def widget_context(self):
        try:
            panel_section = self.record['page_section']
            panel_item = self.record['page_panel']
        except (KeyError, TypeError):
            panel_section = 'main'
            panel_item = '0'
        return {
            'panel_page_section': panel_section,
            'panel_page_item': panel_item
        }

    def widget_uid(self):
        try:
            widget_id = self.record['id']
        except (KeyError, TypeError):
            widget_id = str(uuid_tool.uuid4())
        return widget_id

    def widget_settings(self):
        widget_identifier = self.settings()['widget_type']
        widget_tool = getUtility(IContentWidgetTool)
        try:
            settings = widget_tool.widget_setup(widget_identifier)
        except KeyError:
            settings = {}
        return settings

    def widget_configuration(self):
        widget_tool = getUtility(IContentWidgetTool)
        widget_id = self.settings()['widget_type']
        try:
            configuration = widget_tool.widget_setup(
                widget_id
            )
        except KeyError:
            configuration = {
                "pkg": "PKG Undefined",
                "id": widget_id,
                "name": widget_id.replace('-', ' ').title(),
                "title": widget_id.replace('-', ' ').title(),
                "category": "more",
                "type": "base"
            }
        return configuration

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
