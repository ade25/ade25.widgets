# -*- coding: utf-8 -*-
"""Module providing base widget"""
import uuid
import uuid as uuid_tool

from Acquisition import aq_inner
from Products.Five import BrowserView
from ade25.widgets.interfaces import IContentWidgets
from plone import api
from plone.api.exc import MissingParameterError


class WidgetImageInline(BrowserView):
    """ Base widget used as placeholder """

    def __call__(self,
                 widget_name='image-inline',
                 widget_type='base',
                 widget_mode='view',
                 widget_data=None,
                 **kw):
        self.params = {
            'widget_name': widget_name,
            'widget_type': widget_type,
            'widget_mode': widget_mode,
            'widget_data': widget_data
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

    def has_content(self):
        if self.widget_text_block():
            return True
        return False

    def widget_uid(self):
        try:
            widget_id = self.record['id']
        except (KeyError, TypeError):
            widget_id = str(uuid_tool.uuid4())
        return widget_id

    def widget_text_block(self):
        try:
            content = self.record['data']['content']['text_column_0']
        except (KeyError, TypeError):
            content = None
        return content


class WidgetImageCover(BrowserView):
    """ Base widget used as placeholder """

    def __call__(self,
                 widget_name='image-cover',
                 widget_type='base',
                 widget_mode='view',
                 widget_data=None,
                 **kw):
        self.params = {
            'widget_name': widget_name,
            'widget_type': widget_type,
            'widget_mode': widget_mode,
            'widget_data': widget_data
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

    def has_content(self):
        if self.widget_image_cover():
            return True
        return False

    def widget_uid(self):
        try:
            widget_id = self.record['id']
        except (KeyError, TypeError):
            widget_id = str(uuid_tool.uuid4())
        return widget_id

    def has_lead_image(self):
        context = aq_inner(self.context)
        try:
            lead_img = context.image
        except AttributeError:
            lead_img = None
        if lead_img is not None:
            return True
        return False

    @staticmethod
    def has_stored_image(image_object):
        context = image_object
        try:
            lead_img = context.image
        except AttributeError:
            lead_img = None
        if lead_img is not None:
            return True
        return False

    def image_scale(self):
        registry_record = api.portal.get_registry_record(
            'ade25.widgets.image_cover_scale'
        )
        widget_content = self.widget_stored_data()
        image_scale = widget_content.get('image_scale', registry_record)
        return image_scale

    @staticmethod
    def _compute_aspect_ratio(scale_name):
        if scale_name.startswith('ratio'):
            return scale_name.split('-')[1].replace(':', '/')
        return '1'

    def image_tag(self, image_uid):
        image = api.content.get(UID=image_uid)
        if self.has_stored_image(image):
            figure = image.restrictedTraverse('@@figure')(
                image_field_name='image',
                caption_field_name='image_caption',
                scale=self.image_scale(),
                aspect_ratio=self._compute_aspect_ratio(self.image_scale()),
                lqip=True,
                lazy_load=True
            )
            return figure
        return None

    def widget_image_cover(self):
        context = aq_inner(self.context)
        storage = IContentWidgets(context)
        content = storage.read_widget(self.widget_uid())
        return content

    def widget_stored_data(self):
        context = aq_inner(self.context)
        try:
            storage = IContentWidgets(context)
            content = storage.read_widget(self.widget_uid())
        except TypeError:
            content = dict()
        return content

    def widget_content(self):
        widget_content = self.widget_stored_data()
        image_uid = widget_content['image']
        if 'image_related' in widget_content:
            related_image_record = widget_content.get('image_related')
            if related_image_record:
                try:
                    related_uid = uuid.UUID(str(related_image_record))
                    image_uid = related_uid
                except ValueError:
                    # TODO: Catch edge cases here if necessary
                    pass
        data = {
            'image': self.image_tag(image_uid),
            'public': widget_content['is_public']
        }
        return data
