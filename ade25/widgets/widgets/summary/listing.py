# -*- coding: utf-8 -*-
"""Module providing content listing widgets"""
import uuid as uuid_tool
from Acquisition import aq_inner, aq_parent
from Products.CMFCore.interfaces import ISiteRoot
from Products.Five import BrowserView
from ade25.panelpage.page import IPage
from plone import api
from plone.app.vocabularies.catalog import KeywordsVocabulary
from plone.i18n.normalizer import IIDNormalizer
from zope.component import queryUtility

from ade25.widgets.interfaces import IContentWidgets
from ade25.widgets import MessageFactory as _


class WidgetContentListing(BrowserView):
    """ Basic context content listing """

    def __call__(
        self,
        widget_name="listing",
        widget_type="listing",
        widget_data=None,
        widget_mode="view",
        **kw
    ):
        self.params = {
            "widget_name": widget_name,
            "widget_type": widget_type,
            "widget_mode": widget_mode,
            "widget_data": widget_data,
        }
        self.has_content = len(self.contained_content_items()) > 0
        return self.render()

    def render(self):
        return self.index()

    @staticmethod
    def normalizer():
        return queryUtility(IIDNormalizer)

    @property
    def edit_mode(self):
        if self.params["widget_mode"] == "edit":
            return True
        return False

    @property
    def record(self):
        return self.params["widget_data"]

    def custom_styles(self):
        if self.record and "styles" in self.record:
            return self.record["styles"]
        else:
            return None

    def card_list_class(self):
        context = aq_inner(self.context)
        css_class = "c-list c-list--default c-list--{}".format(context.UID())
        custom_styles = self.custom_styles()
        if custom_styles:
            class_container = custom_styles["class_container"]
            for class_name in class_container.split(" "):
                css_class = "{0} c-list--{1}".format(css_class, class_name)
            if "custom" in custom_styles:
                css_class = "{0} {1}".format(css_class, custom_styles["custom"])
        return css_class

    def widget_uid(self):
        try:
            widget_id = self.record["id"]
        except (KeyError, TypeError):
            widget_id = str(uuid_tool.uuid4())
        return widget_id

    def card_subject_classes(self, item):
        subjects = item.Subject
        class_list = [self.filter_value(keyword) for keyword in subjects]
        return class_list

    def card_css_classes(self, item):
        class_list = self.card_subject_classes(item)
        if class_list:
            return " ".join(class_list)
        else:
            return "app-tag--all"

    def available_keywords(self):
        context = aq_inner(self.context)
        keyword_vocabulary = KeywordsVocabulary()
        vocabulary = keyword_vocabulary(context)
        return vocabulary

    def normalized_token(self, term):
        return self.normalizer().normalize(term, locale="de")

    def normalized_keywords(self):
        vocabulary = self.available_keywords()
        taxonomy = dict()
        for index, term in enumerate(vocabulary):
            element_value = term.value
            taxonomy[index] = element_value
        return taxonomy

    def filter_value(self, term):
        vocabulary = self.normalized_keywords()
        filter_value = "o-tag--undefined"
        for item_index, item_term in vocabulary.items():
            if item_term == term:
                filter_value = "o-tag--{0}".format(str(item_index))
        return filter_value

    def content_items(self):
        results = []
        display_limit = self.widget_stored_data().get("display_limit", "24")
        brains = self.contained_content_items(limit=display_limit)
        layout_reverse = self.widget_stored_data().get("display_reverse", False)
        for brain in brains:
            results.append(
                {
                    "title": brain.Title,
                    "description": brain.Description,
                    "url": brain.getURL(),
                    "timestamp": brain.Date,
                    "uuid": brain.UID,
                    "css_classes": "o-list__item--{0} {1} {2}".format(
                        brain.UID,
                        "o-list__item--{0}".format(
                            layout_reverse and "reverse" or "default"
                        ),
                        self.card_css_classes(brain),
                    ),
                }
            )
        return results

    @staticmethod
    def _get_acquisition_chain(context_object):
        """
        @return: List of objects from context, its parents to the portal root
        Example::
            chain = getAcquisitionChain(self.context)
            print "I will look up objects:" + str(list(chain))
        @param object: Any content object
        @return: Iterable of all parents from the direct parent to the site root
        """

        # It is important to use inner to bootstrap the traverse,
        # or otherwise we might get surprising parents
        # E.g. the context of the view has the view as the parent
        # unless inner is used
        inner = context_object.aq_inner

        content_node = inner

        while content_node is not None:
            yield content_node

            if ISiteRoot.providedBy(content_node):
                break
            if not hasattr(content_node, "aq_parent"):
                raise RuntimeError(
                    "Parent traversing interrupted by object: {}".format(
                        str(content_node)
                    )
                )
            content_node = content_node.aq_parent

    def _base_query(self):
        context = aq_inner(self.context)
        return dict(
            portal_type=[
                "ade25.sitecontent.contentpage",
                "ade25.sitecontent.sectionfolder",
            ],
            path=dict(query="/".join(context.getPhysicalPath()), depth=1),
            review_state="published",
            sort_on="getObjPositionInParent",
        )

    def contained_content_items(self, limit=20):
        context = aq_inner(self.context)
        container = context
        catalog = api.portal.get_tool(name="portal_catalog")
        query = self._base_query()
        query["sort_limit"] = limit
        if IPage.providedBy(container):
            container = aq_parent(container)
        query["path"] = dict(query="/".join(container.getPhysicalPath()), depth=1)
        items = catalog.searchResults(query)[:limit]
        return items

    def widget_stored_data(self):
        context = aq_inner(self.context)
        try:
            storage = IContentWidgets(context)
            content = storage.read_widget(self.widget_uid())
        except TypeError:
            content = dict()
        return content

    def get_widget_content(self, entry, fallback):
        widget_content = self.widget_stored_data()
        try:
            entry_value = self.record['entry']
        except KeyError:
            entry_value = widget_content.get(entry, fallback)
        return entry_value

    def widget_content(self):
        widget_content = self.widget_stored_data()
        data = {
            "title": self.get_widget_content("title", None),
            "batch": self.get_widget_content("display_batch", False),
            "images": self.get_widget_content("display_images", True),
            "abstract": self.get_widget_content("display_abstract", True),
            "limit": self.get_widget_content("display_limit", None),
            "read_more": self.get_widget_content("display_read_more", True),
            "read_more_value": self.get_widget_content(
                "read_more_text", _(u"Read more")
            ),
            "read_more_layout": self.get_widget_content(
                "read_more_layout", "width-33"
            ),
            "layout": self.get_widget_content("display_reverse", False),
            "items": self.content_items(),
        }
        return data


class WidgetContentListingCards(BrowserView):
    """ Basic context content listing displying a card grid"""

    def __call__(self, widget_data=None, widget_mode="view", **kw):
        self.params = {"widget_mode": widget_mode, "widget_data": widget_data}
        self.has_content = len(self.contained_content_items()) > 0
        return self.render()

    def render(self):
        return self.index()

    @staticmethod
    def normalizer():
        return queryUtility(IIDNormalizer)

    @property
    def edit_mode(self):
        if self.params["widget_mode"] == "edit":
            return True
        return False

    @property
    def record(self):
        return self.params["widget_data"]

    def custom_styles(self):
        if self.record and "styles" in self.record:
            return self.record["styles"]
        else:
            return None

    def card_list_class(self):
        context = aq_inner(self.context)
        css_class = "c-list c-list--gutter c-list--grid c-list--{}".format(
            context.UID()
        )
        custom_styles = self.custom_styles()
        if custom_styles:
            class_container = custom_styles["class_container"]
            for class_name in class_container.split(" "):
                css_class = "{0} c-list--{1}".format(css_class, class_name)
            if "custom" in custom_styles:
                css_class = "{0} {1}".format(css_class, custom_styles["custom"])
        return css_class

    def widget_uid(self):
        try:
            widget_id = self.record["id"]
        except (KeyError, TypeError):
            widget_id = str(uuid_tool.uuid4())
        return widget_id

    def card_subject_classes(self, item):
        subjects = item.Subject
        class_list = [self.filter_value(keyword) for keyword in subjects]
        return class_list

    def card_css_classes(self, item):
        class_list = self.card_subject_classes(item)
        if class_list:
            return " ".join(class_list)
        else:
            return "o-tag--all"

    def available_keywords(self):
        context = aq_inner(self.context)
        keyword_vocabulary = KeywordsVocabulary()
        vocabulary = keyword_vocabulary(context)
        return vocabulary

    def normalized_token(self, term):
        return self.normalizer().normalize(term, locale="de")

    def normalized_keywords(self):
        vocabulary = self.available_keywords()
        taxonomy = dict()
        for index, term in enumerate(vocabulary):
            element_value = term.value
            taxonomy[index] = element_value
        return taxonomy

    def filter_value(self, term):
        vocabulary = self.normalized_keywords()
        filter_value = "o-tag--undefined"
        for item_index, item_term in vocabulary.items():
            if item_term == term:
                filter_value = "o-tag--{0}".format(str(item_index))
        return filter_value

    def content_items(self):
        results = []
        display_limit = int(self.widget_stored_data().get("display_limit", "24"))
        brains = self.contained_content_items(limit=display_limit)
        for brain in brains:
            results.append(
                {
                    "title": brain.Title,
                    "description": brain.Description,
                    "url": brain.getURL(),
                    "timestamp": brain.Date,
                    "uuid": brain.UID,
                    "css_classes": "c-card-list__item--{0} {1} {2}".format(
                        brain.UID,
                        "c-card-list__item--{0}".format(
                            self.widget_stored_data().get(
                                "display_columns", "width-100"
                            )
                        ),
                        self.card_css_classes(brain),
                    ),
                }
            )
        return results

    def _base_query(self):
        context = aq_inner(self.context)
        return dict(
            portal_type=[
                "ade25.sitecontent.contentpage",
                "ade25.sitecontent.sectionfolder",
            ],
            path=dict(query="/".join(context.getPhysicalPath()), depth=1),
            review_state="published",
            sort_on="getObjPositionInParent",
        )

    def contained_content_items(self, limit=20):
        context = aq_inner(self.context)
        container = context
        catalog = api.portal.get_tool(name="portal_catalog")
        query = self._base_query()
        query["sort_limit"] = limit
        if IPage.providedBy(container):
            container = aq_parent(container)
        query["path"] = dict(query="/".join(container.getPhysicalPath()), depth=1)
        items = catalog.searchResults(query)[:limit]
        return items

    def widget_stored_data(self):
        context = aq_inner(self.context)
        try:
            storage = IContentWidgets(context)
            content = storage.read_widget(self.widget_uid())
        except TypeError:
            content = dict()
        return content

    def get_widget_content(self, entry, fallback):
        widget_content = self.widget_stored_data()
        try:
            entry_value = self.record['entry']
        except KeyError:
            entry_value = widget_content.get(entry, fallback)
        return entry_value

    def widget_content(self):
        translation_service = api.portal.get_tool(name="translation_service")
        widget_content = self.widget_stored_data()
        data = {
            "title": self.get_widget_content("title", None),
            "batch": self.get_widget_content("display_batch", False),
            "images": self.get_widget_content("display_images", True),
            "abstract": self.get_widget_content("display_abstract", True),
            "limit": self.get_widget_content("display_limit", None),
            "read_more": self.get_widget_content("display_read_more", True),
            "read_more_value": self.get_widget_content(
                "read_more_text",
                translation_service.translate(
                    "Read more",
                    "ade25.widgets",
                    target_language=api.portal.get_default_language(),
                )
            ),
            "read_more_layout": self.get_widget_content("read_more_layout", "link"),
            "image_scale": self.get_widget_content("image_scale", "ratio-4:3"),
            "display_columns": self.get_widget_content("display_columns", "width-33"),
            "items": self.content_items(),
        }
        return data


class FilterableCardListingWidget(BrowserView):
    """ Basic context content listing """

    def __call__(self, widget_data=None, widget_mode="view", **kw):
        self.params = {"widget_mode": widget_mode, "widget_data": widget_data}
        self.has_content = len(self.contained_content_items()) > 0
        return self.render()

    def render(self):
        return self.index()

    def contained_content_items(self):
        context = aq_inner(self.context)
        items = api.content.find(
            context=context,
            depth=1,
            portal_type=[
                "ade25.sitecontent.contentpage",
                "ade25.sitecontent.sectionfolder",
            ],
            review_state="published",
        )
        return items
