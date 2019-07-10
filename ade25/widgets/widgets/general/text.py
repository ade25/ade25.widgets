# -*- coding: utf-8 -*-
"""Module providing base widget"""
import uuid as uuid_tool

from Acquisition import aq_inner
from Products.Five import BrowserView
from ade25.widgets.interfaces import IContentWidgets


class WidgetText(BrowserView):
    """ Base widget used as placeholder """

    def __call__(self,
                 widget_name='text-block',
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


class WidgetTextFormatted(BrowserView):
    """ Base widget used as placeholder """

    def __call__(self,
                 widget_name='text-block',
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
        if self.widget_text_formatted():
            return True
        return False

    def widget_uid(self):
        try:
            widget_id = self.record['id']
        except (KeyError, TypeError):
            widget_id = str(uuid_tool.uuid4())
        return widget_id

    def widget_text_formatted(self):
        context = aq_inner(self.context)
        storage = IContentWidgets(context)
        content = storage.read_widget(self.widget_uid())
        return content

    def widget_content(self):
        widget_content = self.widget_text_formatted()
        data = {
            'text': widget_content['text']
        }
        return data


class WidgetTextHtml(BrowserView):
    """ HTML Text block widget """

    def __call__(self,
                 widget_name='text-block',
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
        if self.widget_text_html():
            return True
        return False

    def widget_uid(self):
        try:
            widget_id = self.record['id']
        except (KeyError, TypeError):
            widget_id = str(uuid_tool.uuid4())
        return widget_id

    def widget_text_html(self):
        context = aq_inner(self.context)
        storage = IContentWidgets(context)
        content = storage.read_widget(self.widget_uid())
        return content

    def widget_content(self):
        widget_content = self.widget_text_html()
        data = {
            'text': widget_content['text']
        }
        return data
