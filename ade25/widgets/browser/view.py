# -*- coding: utf-8 -*-
"""Module providing views for the folderish content page type"""
from Acquisition import aq_inner
from Products.Five.browser import BrowserView


class WidgetView(BrowserView):
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
        context = aq_inner(self.context)
        view_name = '@@content-widget-'.format(
            self.params['identifier'],
        )
        rendered_widget = context.restrictedTraverse(view_name)(self.params)
        return rendered_widget

