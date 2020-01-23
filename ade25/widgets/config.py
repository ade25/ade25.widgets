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
        "schema": "ade25.widgets.widgets.content.interfaces.IAde25WidgetSeparator",  # noqa
        "node": {}
    },
    "horizontal-line": {
        "pkg": "ade25.widgets",
        "id": "horizontal-line",
        "name": "Horizontal Line",
        "title": "Horizontal Line",
        "category": "general",
        "type": "content-item",
        "schema": "ade25.widgets.widgets.content.interfaces.IAde25WidgetHorizontalLine",  # noqa
        "node": {}
    },
    "text-block": {
        "pkg": "ade25.widgets",
        "id": "text-block",
        "name": "Text Block",
        "title": "Text Block",
        "category": "general",
        "type": "content-item",
        "schema": "ade25.widgets.widgets.content.interfaces.IAde25WidgetTextBlock",  # noqa
        "node": {}
    },
    "text-formatted": {
        "pkg": "ade25.widgets",
        "id": "text-formatted",
        "name": "Text Block Formatted",
        "title": "Text Block Formatted",
        "category": "general",
        "type": "content-item",
        "schema": "ade25.widgets.widgets.content.interfaces.IAde25WidgetTextFormatted",  # noqa
        "node": {}
    },
    "text-html": {
        "pkg": "ade25.widgets",
        "id": "text-html",
        "name": "Text Block HTML",
        "title": "Text Block HTML",
        "category": "general",
        "type": "content-item",
        "schema": "ade25.widgets.widgets.content.interfaces.IAde25WidgetTextHtml",  # noqa
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
    "ade25-content-alias": {
        "pkg": "ade25.widgets",
        "id": "ade25-content-alias",
        "name": "HfPH Content Alias",
        "title": "Content Alias",
        "category": "more",
        "type": "content-item",
        "schema": "ade25.widgets.widgets.content.interfaces.IAde25WidgetContentAlias",  # noqa
        "node": {}
    },
    "ade25-teaser-events": {
        "pkg": "ade25.widgets",
        "id": "ade25-teaser-events",
        "name": "HfPH Teaser Events",
        "title": "Teaser Events",
        "category": "more",
        "type": "content-item",
        "schema": "ade25.widgets.widgets.teaser.interfaces.IAde25WidgetTeaserEvents",  # noqa
        "node": {}
    },
    "ade25-teaser-links": {
        "pkg": "ade25.widgets",
        "id": "ade25-teaser-links",
        "name": "HfPH Teaser Links",
        "title": "Teaser Links Internal",
        "category": "more",
        "type": "collection",
        "schema": "ade25.widgets.widgets.teaser.interfaces.IAde25WidgetTeaserLinksInternal",  # noqa
        "node": {
            "title": "Teaser Internal Link",
            "schema": "ade25.widgets.widgets.teaser.interfaces.IAde25WidgetLinkInternal"  # noqa
        }
    },
    "ade25-teaser-external": {
        "pkg": "ade25.widgets",
        "id": "ade25-teaser-links-external",
        "name": "HfPH Teaser Links External",
        "title": "Teaser Links External",
        "category": "more",
        "type": "collection",
        "schema": "ade25.widgets.widgets.teaser.interfaces.IAde25WidgetTeaserLinksExternal",  # noqa
        "node": {
            "title": "External Link",
            "schema": "ade25.widgets.widgets.teaser.interfaces.IAde25WidgetLinkExternal"  # noqa
        }
    },
    "ade25-base-accordion": {
        "pkg": "ade25.widgets",
        "id": "ade25-accordion",
        "name": "HfPH Accordion",
        "title": "Accordion",
        "category": "more",
        "type": "collection",
        "schema": "ade25.widgets.widgets.accordion.interfaces.IAde25WidgetAccordion",  # noqa
        "node": {
            "title": "Pane",
            "schema": "ade25.widgets.widgets.accordion.interfaces.IAde25WidgetAccordionItem"  # noqa
        }
    },
    "ade25-base-slider": {
        "pkg": "ade25.widgets",
        "id": "ade25-slider",
        "name": "HfPH Slider",
        "title": "Slider",
        "category": "more",
        "type": "collection",
        "schema": "ade25.widgets.widgets.slider.interfaces.IAde25WidgetSlider",  # noqa
        "node": {
            "title": "Slide",
            "schema": "ade25.widgets.widgets.slider.interfaces.IAde25WidgetSliderItem"  # noqa
        }
    }
}
