# -*- coding: utf-8 -*-
"""Module providing views for the folderish content page type"""
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
            'widget_data': data_set
        }
        return self.render()

    def render(self):
        return self.rendered_widget()

    def rendered_widget(self):
        context = aq_inner(self.context)
        if self.params['widget_name']:
            view_name = '@@content-widget-{0}'.format(
                self.params['widget_name'],
            )
            rendered_widget = context.restrictedTraverse(view_name)(self.params)
        else:
            view_name = '@@content-widget-base'
            rendered_widget = context.restrictedTraverse(view_name)()
        return rendered_widget
