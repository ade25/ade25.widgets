# -*- coding: utf-8 -*-
"""Module providing base widget"""
from Products.Five import BrowserView
from plone import api


class BaseWidgetView(BrowserView):
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


class BaseWidgetError(BrowserView):
    """ Base widget used as placeholder """

    def __call__(self,
                 widget_name='error',
                 widget_type='error',
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

    @staticmethod
    def can_edit():
        return not api.user.is_anonymous()

    def display_widget(self):
        if self.edit_mode and not api.user.is_anonymous():
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
