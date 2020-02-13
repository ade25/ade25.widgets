# -*- coding: utf-8 -*-
"""Module providing views for the folderish content page type"""
import uuid as uuid_tool
from Acquisition import aq_inner
from Products.Five.browser import BrowserView


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
            'widget_data': data_set,
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
            try:
                rendered_widget = context.restrictedTraverse(view_name)(
                    widget_mode=self.params['widget_mode'],
                    widget_data=self.params['widget_data']
                )
            except:
                view_name = '@@content-widget-error'
                rendered_widget = context.restrictedTraverse(view_name)(
                    widget_mode=self.params['widget_mode'],
                    widget_data=self.params['widget_data']
                )
        else:
            view_name = '@@content-widget-base'
            rendered_widget = context.restrictedTraverse(view_name)()
        return rendered_widget
