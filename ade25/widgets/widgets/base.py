# -*- coding: utf-8 -*-
"""Module providing base widget"""
from Products.Five import BrowserView


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
