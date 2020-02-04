# -*- coding: utf-8 -*-
"""Module providing widget setting constants"""

PKG_WIDGETS = {
    "separator": {
        "pkg": "ade25.widgets",
        "id": "separator",
        "name": "Separator",
        "title": "Separator",
        "category": "general",
        "type": "content-item",
        "schema": "ade25.widgets.widgets.general.interfaces.IAde25WidgetSeparator",  # noqa
        "node": {}
    },
    "horizontal-line": {
        "pkg": "ade25.widgets",
        "id": "horizontal-line",
        "name": "Horizontal Line",
        "title": "Horizontal Line",
        "category": "general",
        "type": "content-item",
        "schema": "ade25.widgets.widgets.general.interfaces.IAde25WidgetHorizontalLine",  # noqa
        "node": {}
    },
    "text-block": {
        "pkg": "ade25.widgets",
        "id": "text-block",
        "name": "Text Block",
        "title": "Text Block",
        "category": "general",
        "type": "content-item",
        "schema": "ade25.widgets.widgets.general.interfaces.IAde25WidgetTextBlock",  # noqa
        "node": {}
    },
    "text-formatted": {
        "pkg": "ade25.widgets",
        "id": "text-formatted",
        "name": "Text Block Formatted",
        "title": "Text Block Formatted",
        "category": "general",
        "type": "content-item",
        "schema": "ade25.widgets.widgets.general.interfaces.IAde25WidgetTextFormatted",  # noqa
        "node": {}
    },
    "text-html": {
        "pkg": "ade25.widgets",
        "id": "text-html",
        "name": "Text Block HTML",
        "title": "Text Block HTML",
        "category": "general",
        "type": "content-item",
        "schema": "ade25.widgets.widgets.general.interfaces.IAde25WidgetTextHtml",  # noqa
        "node": {}
    },
    "image-cover": {
        "pkg": "ade25.widgets",
        "id": "image-cover",
        "name": "Cover Image",
        "title": "Cover Image",
        "category": "image",
        "type": "content-item",
        "schema": "ade25.widgets.widgets.image.interfaces.IAde25WidgetImageCover",  # noqa
        "node": {}
    },
    "image-poster": {
        "pkg": "ade25.widgets",
        "id": "image-poster",
        "name": "Poster Image",
        "title": "Poster Image",
        "category": "image",
        "type": "content-item",
        "schema": "ade25.widgets.widgets.image.interfaces.IAde25WidgetImagePoster",  # noqa
        "node": {}
    },
    "slider": {
        "pkg": "ade25.widgets",
        "id": "slider",
        "name": "Slider",
        "title": "Slider",
        "category": "gallery",
        "type": "collection",
        "schema": "ade25.widgets.widgets.gallery.slider.interfaces.IAde25WidgetSlider",  # noqa
        "node": {
            "title": "Slide",
            "schema": "ade25.widgets.widgets.gallery.slider.interfaces.IAde25WidgetSliderItem"  # noqa
        }
    },
    "listing": {
        "pkg": "ade25.widgets",
        "id": "listing",
        "name": "Content Listing",
        "title": "Content Listing",
        "category": "summary",
        "type": "content-item",
        "schema": "ade25.widgets.widgets.summary.interfaces.IAde25WidgetListing",  # noqa
        "node": {}
    },
    "listing-cards": {
        "pkg": "ade25.widgets",
        "id": "listing-cards",
        "name": "Content Cards",
        "title": "Content Cards",
        "category": "summary",
        "type": "content-item",
        "schema": "ade25.widgets.widgets.summary.interfaces.IAde25WidgetListingCards",  # noqa
        "node": {}
    },
    "accordion": {
        "pkg": "ade25.widgets",
        "id": "accordion",
        "name": "HfPH Accordion",
        "title": "Accordion",
        "category": "more",
        "type": "collection",
        "schema": "ade25.widgets.widgets.more.accordion.interfaces.IAde25WidgetAccordion",  # noqa
        "node": {
            "title": "Pane",
            "schema": "ade25.widgets.widgets.more.accordion.interfaces.IAde25WidgetAccordionItem"  # noqa
        }
    }
}
