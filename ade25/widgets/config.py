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
        "schemata": [],
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
        "schemata": [],
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
        "schemata": [],
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
        "schemata": [],
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
        "schemata": [],
        "node": {}
    },
    "page-header": {
        "pkg": "ade25.widgets",
        "id": "page-header",
        "name": "Page Header",
        "title": "Page Header",
        "category": "general",
        "type": "content-item",
        "schema": "ade25.widgets.widgets.general.interfaces.IAde25WidgetPageHeader",  # noqa
        "schemata": [],
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
        "schemata": [],
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
        "schemata": ["ade25.widgets.widgets.interfaces.IAde25WidgetPartialContentMain"],
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
        "schemata": [],
        "node": {
            "title": "Slide",
            "schema": "ade25.widgets.widgets.gallery.slider.interfaces.IAde25WidgetSliderItem",  # noqa
            "schemata": [],
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
        "schemata": [],
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
        "schemata": [],
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
        "schemata": [],
        "node": {
            "title": "Pane",
            "schema": "ade25.widgets.widgets.more.accordion.interfaces.IAde25WidgetAccordionItem",  # noqa
            "schemata": [],
        }
    }
}

# Limited TinyMCe editor options
# Usage:
# directives.widget(
#     "text",
#     RichTextFieldWidget,
#     pattern_options=TINY_MCE_LIGHT_OPTIONS
# )
# text = RichTextField(
#     title="Text",
#     required=False,
# )

TINY_MCE_LIGHT_OPTIONS = {
    "tiny": {
        "menu": {
            "edit": {
                "items": "undo redo",
                "title": "Edit",
            },
            "format": {
                "items": "bold italic underline | formats",
                "title": "Format",
            },
            "insert": {"items": "hr", "title": "Insert"},
            "table": {
                "items": "",
                "title": "Table",
            },
            "tools": {
                "items": "code",
                "title": "Tools",
            },
            "view": {
                "items": "",
                "title": "View",
            },
        },
        "menubar": ["edit", "table", "format", "toolsview", "insert"],
        "toolbar": "undo redo | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent",
        "plugins": [
            "hr",
            "lists",
            "nonbreaking",
            "noneditable",
            "pagebreak",
            "paste",
            "code",
        ],
        "style_formats": [
            {
                "items": [
                    {"format": "h2", "title": "Header 2"},
                    {"format": "h3", "title": "Header 3"},
                    {"format": "h4", "title": "Header 4"},
                    {"format": "h5", "title": "Header 5"},
                    {"format": "h6", "title": "Header 6"},
                ],
                "title": "Headers",
            },
            {
                "items": [
                    {"format": "p", "title": "Paragraph"},
                    {"format": "blockquote", "title": "Blockquote"},
                    {"format": "div", "title": "Div"},
                    {"format": "pre", "title": "Pre"},
                ],
                "title": "Block",
            },
            {
                "items": [
                    {"format": "bold", "icon": "bold", "title": "Bold"},
                    {"format": "italic", "icon": "italic", "title": "Italic"},
                    {
                        "format": "underline",
                        "icon": "underline",
                        "title": "Underline",
                    },
                    {
                        "format": "strikethrough",
                        "icon": "strikethrough",
                        "title": "Strikethrough",
                    },
                    {
                        "format": "superscript",
                        "icon": "superscript",
                        "title": "Superscript",
                    },
                    {
                        "format": "subscript",
                        "icon": "subscript",
                        "title": "Subscript",
                    },
                    {"format": "code", "icon": "code", "title": "Code"},
                ],
                "title": "Inline",
            },
            {
                "items": [
                    {
                        "format": "alignleft",
                        "icon": "alignleft",
                        "title": "Left",
                    },
                    {
                        "format": "aligncenter",
                        "icon": "aligncenter",
                        "title": "Center",
                    },
                    {
                        "format": "alignright",
                        "icon": "alignright",
                        "title": "Right",
                    },
                    {
                        "format": "alignjustify",
                        "icon": "alignjustify",
                        "title": "Justify",
                    },
                ],
                "title": "Alignment",
            },
            {
                "items": [
                    {
                        "classes": "listing",
                        "selector": "table",
                        "title": "Listing",
                    }
                ],
                "title": "Tables",
            },
        ],
    }
}
