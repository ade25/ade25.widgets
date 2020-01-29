# -*- coding: utf-8 -*-
"""Module providing preview cards"""
import uuid as uuid_tool
from Acquisition import aq_inner
from Products.Five import BrowserView
from plone import api
from plone.i18n.normalizer import IIDNormalizer
from zope.component import queryUtility


class WidgetContentReadMore(BrowserView):
    """ Basic read more lin widget"""

    def __call__(
        self,
        widget_name="read-more",
        widget_type="read-more",
        widget_data=None,
        widget_mode="view",
        **kw
    ):
        self.params = {"widget_mode": widget_mode, "widget_data": widget_data}
        return self.render()

    def render(self):
        return self.index()

    @staticmethod
    def can_edit():
        return not api.user.is_anonymous()

    @property
    def record(self):
        return self.params["widget_data"]

    def css_classes(self):
        base_class = "o-read-more"
        element_classes = {
            "link": "o-read-more--default",
            "link-icon": "o-read-more--grid",
            "link-icon-prefix": "o-read-more--inverse",
            "icon": "o-read-more--default",
            "button": "o-read-more--default",
            "button-icon": "o-read-more--grid",
            "button-icon-prefix": "o-read-more--inverse",
        }
        element_class = "{0} {1}".format(
            base_class,
            element_classes.get(
                self.record.get("read_more_layout", "link"), "o-read-more--default"
            ),
        )
        return element_class


class WidgetContentCard(BrowserView):
    """ Basic context content card """

    def __call__(
        self,
        widget_name="content-card",
        widget_type="content-card",
        widget_data=None,
        widget_mode="view",
        **kw
    ):
        self.params = {"widget_mode": widget_mode, "widget_data": widget_data}
        return self.render()

    def render(self):
        return self.index()

    @staticmethod
    def can_edit():
        return not api.user.is_anonymous()

    @property
    def record(self):
        return self.params["widget_data"]

    def has_content(self):
        if self.widget_content():
            return True
        return False

    def widget_uid(self):
        try:
            widget_id = self.record["id"]
        except (KeyError, TypeError):
            widget_id = str(uuid_tool.uuid4())
        return widget_id

    @staticmethod
    def normalizer():
        return queryUtility(IIDNormalizer)

    def card_subject_classes(self, item):
        context = item
        subjects = context.Subject()
        class_list = [
            "app-card-tag--{0}".format(self.normalizer().normalize(keyword))
            for keyword in subjects
        ]
        return class_list

    def card_css_classes(self, item):
        class_list = self.card_subject_classes(item)
        if class_list:
            return " ".join(class_list)
        else:
            return "app-card-tag--all"

    @staticmethod
    def has_image(context):
        try:
            lead_img = context.image
        except AttributeError:
            lead_img = None
        if lead_img is not None:
            return True
        return False

    def widget_content(self):
        context = aq_inner(self.context)
        widget_data = self.params["widget_data"]
        if widget_data and "uuid" in widget_data:
            context = api.content.get(UID=widget_data["uuid"])
        details = {
            "title": context.Title(),
            "description": context.Description(),
            "url": context.absolute_url(),
            "timestamp": context.Date,
            "uuid": context.UID(),
            "has_image": self.has_image(context),
            "css_classes": "app-card--{0} {1}".format(
                context.UID(), self.card_css_classes(context)
            ),
            "content_item": context,
        }
        return details


class WidgetContentSnippet(BrowserView):
    """ Basic context content snippet """

    def __call__(
        self,
        widget_name="content-snippet",
        widget_type="content-snippet",
        widget_data=None,
        widget_mode="view",
        **kw
    ):
        self.params = {"widget_mode": widget_mode, "widget_data": widget_data}
        return self.render()

    def render(self):
        return self.index()

    @staticmethod
    def can_edit():
        return not api.user.is_anonymous()

    @property
    def record(self):
        return self.params["widget_data"]

    def has_content(self):
        if self.widget_content():
            return True
        return False

    def widget_uid(self):
        try:
            widget_id = self.record["id"]
        except (KeyError, TypeError):
            widget_id = str(uuid_tool.uuid4())
        return widget_id

    @staticmethod
    def normalizer():
        return queryUtility(IIDNormalizer)

    def card_subject_classes(self, item):
        context = item
        subjects = context.Subject()
        class_list = [
            "o-tag--{0}".format(self.normalizer().normalize(keyword))
            for keyword in subjects
        ]
        return class_list

    def card_css_classes(self, item):
        class_list = self.card_subject_classes(item)
        snippet_layout = self.record.get("snippet_layout", "default")
        class_list.append('c-snippet--{0}'.format(snippet_layout))
        if class_list:
            return " ".join(class_list)
        else:
            return "o-tag--all"

    @staticmethod
    def has_image(context):
        try:
            lead_img = context.image
        except AttributeError:
            lead_img = None
        if lead_img is not None:
            return True
        return False

    def widget_content(self):
        context = aq_inner(self.context)
        widget_data = self.params["widget_data"]
        if "uuid" in widget_data:
            context = api.content.get(UID=widget_data["uuid"])
        details = {
            "title": context.Title(),
            "description": context.Description(),
            "url": context.absolute_url(),
            "timestamp": context.Date,
            "uuid": context.UID(),
            "has_image": self.has_image(context),
            "css_classes": "c-snippet--{0} {1}".format(
                context.UID(), self.card_css_classes(context)
            ),
            "content_item": context,
        }
        return details

    @staticmethod
    def _compute_aspect_ratio(scale_name):
        if scale_name.startswith('ratio'):
            return scale_name.split('-')[1].replace(':', '/')
        return scale_name

    def figure_configuration(self):
        requested_scale = self.record.get("image_scale", "ratio-4:3")
        settings = {
            "scale": requested_scale,
            "ratio": self._compute_aspect_ratio(requested_scale)
        }
        return settings

    @staticmethod
    def _read_more_text_default():
        translation_service = api.portal.get_tool(name="translation_service")
        default_text = translation_service.translate(
            "Read more",
            "ade25.widgets",
            target_language=api.portal.get_default_language(),
        )
        return default_text

    def _read_more_symbol(self):
        layout = self.record.get("read_more_layout", "link")
        if 'icon' in layout:
            return True
        return False

    def read_more_link(self):
        context = aq_inner(self.context)
        widget_configuration = dict(
            read_more_layout=self.record.get("read_more_layout", "link"),
            read_more_position=self.record.get("read_more_position", "left"),
            read_more_text=self.record.get("read_more_text", True),
            read_more_text_value=self.record.get(
                "read_more_text_value", self._read_more_text_default()
            ),
            read_more_symbol=self._read_more_symbol(),
            read_more_symbol_icon=self.record.get("read_more_symbol_icon", "chevron"),
        )
        rendered_widget = context.restrictedTraverse("@@content-widget-read-more")(
            widget_data=widget_configuration
        )
        return rendered_widget
