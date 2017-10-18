# -*- coding: utf-8 -*-
"""Module providing views for the folderish content page type"""
from Products.Five.browser import BrowserView


class WidgetView(BrowserView):
    """ Default widget view

    Renders the provided template and view by the widget in question
    """
