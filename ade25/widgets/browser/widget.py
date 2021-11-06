# -*- coding: utf-8 -*-
"""Module providing widget editor and view"""
import hashlib
import uuid
import uuid as uuid_tool

from Acquisition import aq_inner
from ade25.panelpage.interfaces import IPanelEditor
from plone import api
from plone.api.exc import InvalidParameterError
from plone.autoform.form import AutoExtensibleForm
from plone.namedfile.interfaces import INamedBlobImage
from plone.protect.utils import addTokenToUrl
from plone.supermodel import model
from plone.z3cform.layout import FormWrapper
from z3c.form import button
from z3c.form import form
from z3c.form.interfaces import HIDDEN_MODE, NOT_CHANGED
from z3c.relationfield import RelationValue
from z3c.relationfield.interfaces import IRelationValue
from zope import schema, component
from zope.component import getUtility
from zope.dottedname.resolve import resolve
from zope.interface import implementer
from zope.intid import IIntIds
from zope.lifecycleevent import modified
from zope.publisher.interfaces import IPublishTraverse


from ade25.widgets.interfaces import IContentWidgetTool, IContentWidgets
from ade25.widgets import MessageFactory as _
from zope.schema import getFieldsInOrder


class IContentWidgetSettings(model.Schema):

    is_public = schema.Bool(
        title=_(u"This widget is public and will be displayed in the page "
                u"view"),
        default=True,
        required=False
    )


@implementer(IPublishTraverse)
class ContentWidgetForm(AutoExtensibleForm, form.Form):
    """This search form enables you to find users by specifying one or more
    search criteria.
    """

    schema = IContentWidgetSettings
    ignoreContext = False
    css_class = 'o-form o-form--widget'

    label = _(u'Content Widget')
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
            additional_interfaces = editor_data['widget_settings'].get('schemata', [])
            for additional_interface in additional_interfaces:
                schemata += (resolve(additional_interface),)
            return schemata
        except ValueError:
            return ()

    def getContent(self):
        context = aq_inner(self.context)
        editor_data = self.panel_editor[context.UID()]
        storage = IContentWidgets(context)
        stored_widget_data = storage.read_widget(editor_data['widget_id'])
        widget_content = dict()
        if stored_widget_data:
            schemata = self.additionalSchemata + (self.schema, )
            for widget_schema in schemata:
                fields = getFieldsInOrder(widget_schema)
                for key, value in fields:
                    if key == "image":
                        image_uid = stored_widget_data.get("image", None)
                        if image_uid:
                            asset = api.content.get(UID=image_uid)
                            widget_content[key] = getattr(asset, key, value)
                    elif key.endswith('_related'):
                        # Make sure we do not fall over old widget attribute values
                        widget_content[key] = RelationValue(None)
                    else:
                        widget_content[key] = stored_widget_data.get(
                            key,
                            None
                        )
        return widget_content

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
            try:
                rendered_widget = context.restrictedTraverse(view_name)(
                    widget_mode=self.settings()['widget_mode'],
                    widget_data=self.settings()['widget_data']
                )
            except:
                view_name = '@@content-widget-error'
                rendered_widget = context.restrictedTraverse(view_name)()
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
        return hashlib.sha1(
            (str(uuid.uuid4()) + file_name).encode("utf-8")).hexdigest()

    def _process_image_asset(self, field_key, field_value):
        portal = api.portal.get()
        asset_repository = portal['asset-repository']
        widget_file = api.content.create(
            container=asset_repository,
            type="Image",
            id="widget-asset-{0}".format(
                self.generate_hash_from_filename(field_value.filename),
            ),
            title=field_value.filename,
            image=field_value
        )
        modified(widget_file)
        widget_file.reindexObject(idxs='modified')
        return widget_file.UID()

    @staticmethod
    def _process_relations(target_object):
        if target_object:
            int_ids = component.getUtility(IIntIds)
            return RelationValue(int_ids.getId(target_object))
        return RelationValue(None)

    def applyChanges(self, data):
        context = aq_inner(self.context)
        editor_data = self.panel_editor[context.UID()]
        storage = IContentWidgets(context)
        widget_content = dict()
        for key, value in data.items():
            entry_key = self.prettify_key(key)
            # Additional schemata are posted as 'ISchemaInterface.field_name'
            # and need to be resolved to their original key
            field_key = key.split('.')[-1]
            # Handle image like content
            if INamedBlobImage.providedBy(value):
                image_uid = self._process_image_asset(entry_key, value)
                widget_content[entry_key] = image_uid
            else:
                if value is NOT_CHANGED:
                    # Keep existing value for fields signaling as not updated
                    stored_content = editor_data.get('widget_content')
                    if widget_content:
                        value = stored_content.get(field_key, None)
                if entry_key.endswith('_related'):
                    # Handle asset relation choice
                    widget_content[entry_key] = self._process_relations(value)
                    source_entry_key = key.replace('_related', '')
                    source_value = data.get(source_entry_key, None)
                    if not source_value:
                        # Actual image uploads take preference. Only if no image has
                        # been uploaded write relation choice to image field.
                        widget_content[source_entry_key] = value.UID()
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
        self.actions["cancel"].addClass("c-button--default")
        self.actions["update"].addClass("c-button--primary")

    def updateWidgets(self, prefix=None):
        context = aq_inner(self.context)
        editor_data = self.panel_editor[context.UID()]
        widget_type = editor_data['widget_settings']['widget']
        # Hidden fields can be configured via control panel
        try:
            content_widget_hidden_fields = api.portal.get_registry_record(
                'ade25.widgets.{0}_hidden_fields'.format(
                    widget_type.replace('-', '_')
                )
            )
            for field in content_widget_hidden_fields:
                field_name = '{0}.{1}'.format(
                    editor_data['widget_settings']['schema'].split('.')[-1],
                    field
                )
                if self.widgets and field_name in self.widgets:
                    self.widgets[field_name].mode = HIDDEN_MODE
        except InvalidParameterError:
            # The content widget has no a registry setting
            pass
        super(ContentWidgetForm, self).updateWidgets(prefix=None)


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

    @staticmethod
    def panel_editor():
        tool = getUtility(IPanelEditor)
        return tool.get()

    @property
    def configuration(self):
        context = aq_inner(self.context)
        return self.panel_editor()[context.UID()]

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

    @staticmethod
    def widget_actions(content_type="default"):
        actions = [
            "create",
            "update",
            "delete",
            "settings",
        ]
        if content_type == "collection-item":
            actions = [
                "update",
                "remove",
                "reorder"
            ]
        return actions

    def widget_action(self, action_name, widget_type="base"):
        context = aq_inner(self.context)
        widget_tool = getUtility(IContentWidgetTool)
        is_current = False
        if action_name == "update":
            is_current = False
        action_details = widget_tool.widget_action_details(
            context,
            action_name,
            widget_type,
            is_current
        )
        return action_details

    def widget_item_action(self, action_name, widget_type="base"):
        context = aq_inner(self.context)
        widget_tool = getUtility(IContentWidgetTool)
        is_current = False
        if action_name == "update":
            is_current = False
        action_details = widget_tool.widget_action_details(
            context,
            action_name,
            widget_type,
            is_current
        )
        return action_details

    @staticmethod
    def widget_action_url(action_url):
        return addTokenToUrl(action_url)

    def widget_item_nodes(self):
        context = aq_inner(self.context)
        ordered_nodes = list()
        storage = IContentWidgets(context)
        stored_widget = storage.read_widget(
            self.configuration['widget_id']
        )
        if stored_widget:
            ordered_nodes = stored_widget["item_order"]
        return ordered_nodes

    def has_widget_item_nodes(self):
        return len(self.widget_item_nodes()) > 0

    def widget_item_node_is_public(self, node_id):
        context = aq_inner(self.context)
        editor = self.panel_editor()[context.UID()]
        stored_nodes = editor['widget_content'].get('items')
        if stored_nodes:
            widget_node_data = stored_nodes.get(node_id)
            if widget_node_data:
                return widget_node_data.get('is_public', True)
        return True

    def widget_reorder_handler(self):
        context = aq_inner(self.context)
        context_url = context.absolute_url()
        reorder_view = '@@content-widget-collection-reorder'
        widget_identifier = 'section={0}&panel={1}'.format(
            self.widget_context()['panel_page_section'],
            self.widget_context()['panel_page_item']
        )
        reorder_handler = '{base_url}/{view}?{parameter}'.format(
            base_url=context_url,
            view=reorder_view,
            parameter=widget_identifier
        )
        return reorder_handler

    def rendered_widget(self):
        context = aq_inner(self.context)
        if self.settings()['widget_type']:
            view_name = '@@content-widget-{0}'.format(
                self.settings()['widget_type']
            )
            try:
                rendered_widget = context.restrictedTraverse(view_name)(
                    widget_mode=self.settings()['widget_mode'],
                    widget_data=self.settings()['widget_data']
                )
            except:
                view_name = '@@content-widget-error'
                rendered_widget = context.restrictedTraverse(view_name)()
        else:
            view_name = '@@content-widget-base'
            rendered_widget = context.restrictedTraverse(view_name)()
        return rendered_widget
