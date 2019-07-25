# -*- coding: utf-8 -*-
"""Module providing widget item views and forms"""
import hashlib
import uuid
import uuid as uuid_tool

from AccessControl import Unauthorized
from Acquisition import aq_inner
from Products.CMFPlone.utils import safe_unicode
from Products.Five import BrowserView
from ade25.panelpage.interfaces import IPanelEditor
from plone import api
from plone.app.textfield import IRichTextValue
from plone.autoform.form import AutoExtensibleForm
from plone.namedfile.interfaces import INamedBlobImage
from plone.protect.utils import addTokenToUrl
from plone.supermodel import model
from plone.z3cform.layout import FormWrapper
from z3c.form import button
from z3c.form import form
from zope import schema
from zope.component import getUtility, getMultiAdapter
from zope.dottedname.resolve import resolve
from zope.interface import implementer
from zope.lifecycleevent import modified
from zope.publisher.interfaces import IPublishTraverse


from ade25.widgets.interfaces import IContentWidgetTool, IContentWidgets
from ade25.widgets import MessageFactory as _
from zope.schema import getFieldsInOrder


class IContentWidgetItemSettings(model.Schema):

    is_public = schema.Bool(
        title=_(u"Public"),
        description=_(u"Select if this widget should be visible in the view "
                      u"or remain in a draft version."),
        default=True,
        required=False
    )


@implementer(IPublishTraverse)
class ContentWidgetItemForm(AutoExtensibleForm, form.Form):
    """This search form enables you to find users by specifying one or more
    search criteria.
    """

    schema = IContentWidgetItemSettings
    ignoreContext = False
    css_class = 'o-form o-form--widget'

    label = _(u'Content Widget Item')
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
            schema_interface = resolve(
                editor_data['widget_settings']['node']['schema']
            )
            schemata = (schema_interface,)
            return schemata
        except ValueError:
            return ()

    def getContent(self):
        context = aq_inner(self.context)
        editor_data = self.panel_editor[context.UID()]
        widget_node_id = editor_data["widget_node"]
        storage = IContentWidgets(context)
        stored_widget_data = storage.read_widget(editor_data['widget_id'])
        widget_content = dict()
        if stored_widget_data:
            widget_node = stored_widget_data["items"].get(
                widget_node_id,
                None
            )
            if widget_node:
                schemata = self.additionalSchemata + (self.schema, )
                for widget_schema in schemata:
                    fields = getFieldsInOrder(widget_schema)
                    for key, value in fields:
                        if key == "image":
                            image_uid = widget_node.get("image", None)
                            if image_uid:
                                asset = api.content.get(UID=image_uid)
                                widget_content[key] = getattr(asset, key, value)
                        else:
                            widget_content[key] = widget_node.get(
                                key,
                                value.title
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

    @property
    def action(self):
        """ Rewrite HTTP POST action.
#        If the form is rendered embedded on the others pages we
        make sure the form is posted through the same view always,
        instead of making HTTP POST to the page where the form was rendered.
        """
        return self.context.absolute_url() + "/@@content-widget-item-form"

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
                self.generate_hash_from_filename(field_value.filename),
            ),
            image=field_value
        )
        modified(widget_file)
        widget_file.reindexObject(idxs='modified')
        return widget_file.UID()

    def applyChanges(self, data):
        context = aq_inner(self.context)
        editor_data = self.panel_editor[context.UID()]
        storage = IContentWidgets(context)
        record = storage.read_widget(editor_data["widget_id"])
        item_order = record["item_order"]
        if item_order:
            widget_content = record["items"]
        else:
            widget_content = editor_data["widget_content"]
        if not widget_content:
            widget_content = dict()
        widget_item = dict()
        widget_item_node = editor_data["widget_node"]
        for key, value in data.items():
            entry_key = self.prettify_key(key)
            if INamedBlobImage.providedBy(value):
                image_uid = self._process_image_asset(entry_key, value)
                widget_item[entry_key] = image_uid
            elif IRichTextValue.providedBy(value):
                # Handle rich text value that is not serializable
                text_value = value.output
                widget_item[entry_key] = text_value
            else:
                widget_item[entry_key] = value
        if widget_item_node in item_order:
            widget_content[widget_item_node] = widget_item
        else:
            widget_content.update({
                widget_item_node: widget_item
            })
            item_order.append(widget_item_node)
            record["item_order"] = item_order
            record["items"] = widget_content
        storage.store_widget(
            editor_data['widget_id'],
            record,
            self.request
        )
        next_url = '{url}/@@panel-edit?section={section}&panel={panel}'.format(
            url=context.absolute_url(),
            section=editor_data["content_section"],
            panel=editor_data["content_section_panel"]
        )
        return self.request.response.redirect(next_url)

    @button.buttonAndHandler(_(u'cancel'), name='cancel')
    def handleCancel(self, action):
        context = aq_inner(self.context)
        editor_data = self.panel_editor[context.UID()]
        next_url = '{url}/@@panel-edit?section={section}&panel={panel}'.format(
            url=context.absolute_url(),
            section=editor_data["content_section"],
            panel=editor_data["content_section_panel"]
        )
        return self.request.response.redirect(addTokenToUrl(next_url))

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
        super(ContentWidgetItemForm, self).updateActions()
        self.actions["cancel"].addClass(
            "c-button--default c-button--cancel c-button--panel")
        self.actions["update"].addClass("c-button--primary")


class ContentWidgetItemEdit(FormWrapper):

    form = ContentWidgetItemForm

    def __call__(self,
                 nid=None,
                 debug='off',
                 **kw):
        self.params = {
            'node_id': nid,
            'debug_mode': debug
        }
        self._update_panel_editor(self.params)
        self.update()
        return self.render()

    @property
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
        if self.settings['widget_mode'] == 'edit':
            return True
        return False

    @property
    def record(self):
        return self.settings['widget_data']

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
        widget_identifier = self.settings['widget_type']
        widget_tool = getUtility(IContentWidgetTool)
        try:
            settings = widget_tool.widget_setup(widget_identifier)
        except KeyError:
            settings = {}
        return settings

    def widget_configuration(self):
        widget_tool = getUtility(IContentWidgetTool)
        widget_id = self.settings['widget_type']
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

    def widget_item_content(self):
        context = aq_inner(self.context)
        item_content = dict()
        storage = IContentWidgets(context)
        stored_widget = storage.read_widget(
            self.configuration['widget_id']
        )
        if stored_widget:
            content_items = stored_widget["items"]
            if content_items:
                item_content = content_items[self.params["nid"]]
        return item_content

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
                "delete",
                "reorder"
            ]
        return actions

    def widget_action(self, action_name, widget_type="base"):
        context = aq_inner(self.context)
        widget_tool = getUtility(IContentWidgetTool)
        is_current = False
        if action_name == "update":
            is_current = True
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

    def _update_panel_editor(self, settings):
        context = aq_inner(self.context)
        tool = getUtility(IPanelEditor)
        editor_data = tool.get()[context.UID()]
        editor_data["widget_node"] = settings["node_id"]
        return tool.update(
            key=context.UID(),
            data=editor_data
        )

    def panel_editor_close(self):
        context = aq_inner(self.context)
        editor_data = self.panel_editor()[context.UID()]
        next_url = '{url}/@@panel-edit?section={section}&panel={panel}'.format(
            url=context.absolute_url(),
            section=editor_data["content_section"],
            panel=editor_data["content_section_panel"]
        )
        return addTokenToUrl(next_url)

    def rendered_widget(self):
        context = aq_inner(self.context)
        if self.settings['widget_type']:
            view_name = '@@content-widget-{0}'.format(
                self.settings['widget_type']
            )
            rendered_widget = context.restrictedTraverse(view_name)(
                widget_mode=self.settings['widget_mode'],
                widget_data=self.settings['widget_data']
            )
        else:
            view_name = '@@content-widget-base'
            rendered_widget = context.restrictedTraverse(view_name)()
        return rendered_widget


class ContentWidgetItemCreate(BrowserView):
    """ Content widget item create view

    Adds  a single instance of a content collection widget
    """

    def __call__(self,
                 nid=None,
                 debug='off',
                 **kw):
        self.params = {
            'node_id': nid,
            'debug_mode': debug
        }
        return self.render()

    @property
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

    def widget_item_content(self):
        context = aq_inner(self.context)
        item_content = dict()
        storage = IContentWidgets(context)
        stored_widget = storage.read_widget(
            self.configuration['widget_id']
        )
        if stored_widget:
            item_content = stored_widget["items"]
        return item_content

    def _content_widget_factory(self):
        context = aq_inner(self.context)
        tool = getUtility(IPanelEditor)
        editor_data = tool.get()[context.UID()]
        node_uid = str(uuid_tool.uuid4())
        editor_data["widget_node"] = node_uid
        tool.update(
            key=context.UID(),
            data=editor_data
        )
        storage = IContentWidgets(context)
        if not self.widget_item_nodes():
            widget_content = {
                "items": dict(),
                "item_order": list()
            }
            storage.store_widget(
                editor_data['widget_id'],
                widget_content,
                self.request
            )
        return node_uid

    def render(self):
        context = aq_inner(self.context)
        node_uid = self._content_widget_factory()
        next_url = '{0}/@@content-widget-item-edit?nid={1}'.format(
            context.absolute_url(),
            node_uid
        )
        return self.request.response.redirect(addTokenToUrl(next_url))


class ContentWidgetItemRemove(BrowserView):
    """ Content widget item deletion

    Remove a single instance of a content widget node
    """
    errors = dict()

    def __call__(self,
                 nid=None,
                 debug='off',
                 **kw):
        self.params = {
            'node_id': nid,
            'debug_mode': debug
        }
        return self.render()

    @property
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

    def widget_item_records(self):
        context = aq_inner(self.context)
        storage = IContentWidgets(context)
        records = storage.read_widget(
            self.configuration['widget_id']
        )
        return records

    def widget_item_nodes(self):
        ordered_nodes = list()
        stored_widget = self.widget_item_records()
        if stored_widget:
            ordered_nodes = stored_widget["item_order"]
        return ordered_nodes

    def _update_panel_editor(self, editor_data):
        context = aq_inner(self.context)
        tool = getUtility(IPanelEditor)
        return tool.update(
            key=context.UID(),
            data=editor_data
        )

    def _remove_widget(self, form_data):
        context = aq_inner(self.context)
        editor_data = self.panel_editor()
        storage = IContentWidgets(context)
        widget_node_id = form_data.get('nid', None)
        widget_nodes = self.widget_item_nodes()
        if widget_node_id and widget_node_id in widget_nodes:
            records = self.widget_item_records()
            widget_nodes_content = records.get('items', dict())
            del widget_nodes_content[widget_node_id]
            widget_nodes_content.remove(widget_node_id)
            records["item_order"] = widget_nodes
            editor_data['widget_content']['item_order'] = widget_nodes
            records["items"] = widget_nodes_content
            editor_data['widget_content']['items'] = widget_nodes_content
            storage.store_widget(
                editor_data['widget_id'],
                records,
                self.request
            )
            self._update_panel_editor(editor_data)
        next_url = self.panel_editor_close()
        return self.request.response.redirect(next_url)

    def update(self):
        self.errors = dict()
        unwanted = ('_authenticator', 'form.button.Submit')
        required = ('widget_node', )
        if 'form.button.Submit' in self.request:
            authenticator = getMultiAdapter((self.context, self.request),
                                            name=u"authenticator")
            if not authenticator.verify():
                raise Unauthorized
            form = self.request.form
            form_data = {}
            form_data.update(self.params)
            form_errors = {}
            error_idx = 0
            for value in form:
                if value not in unwanted:
                    form_data[value] = safe_unicode(form[value])
                    if not form[value] and value in required:
                        form_errors[value] = self.required_field_error()
                        error_idx += 1
                    else:
                        error = {
                            'active': False,
                            'msg': form[value]
                        }
                        form_errors[value] = error
            if error_idx > 0:
                self.errors = form_errors
            else:
                self._remove_widget(form)

    def render(self):
        self.update()
        return self.index()

    def panel_editor_close(self):
        context = aq_inner(self.context)
        editor_data = self.panel_editor()[context.UID()]
        next_url = '{url}/@@panel-edit?section={section}&panel={panel}'.format(
            url=context.absolute_url(),
            section=editor_data["content_section"],
            panel=editor_data["content_section_panel"]
        )
        return addTokenToUrl(next_url)

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
                "delete",
                "reorder"
            ]
        return actions

    def widget_action(self, action_name, widget_type="base"):
        context = aq_inner(self.context)
        widget_tool = getUtility(IContentWidgetTool)
        is_current = False
        if action_name == "remove":
            is_current = True
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
