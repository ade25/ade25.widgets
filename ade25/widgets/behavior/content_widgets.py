# encoding=utf-8
import json
from hashlib import sha256
from uuid import UUID

from persistent.dict import PersistentDict
from persistent.list import PersistentList
from zope.annotation.interfaces import IAnnotations

# The key must be unique. Using the class name with the complete module name
# is a good idea. But be careful, you might want to change the key if you move
# the location to a different place. Else you won't find your own annotations
KEY = "ade25.widgets.behavior.content_widgets"


class ContentWidgets(object):
    def __init__(self, context):
        self.context = context
        annotations = IAnnotations(context)
        if KEY not in annotations.keys():
            # You know what happens if we don't use persistent classes here?
            annotations[KEY] = PersistentDict({
                "widget_hashes": PersistentList(),
                'widgets': PersistentDict()
            })
        self.annotations = annotations[KEY]

    @staticmethod
    def validate_uuid4(uuid_string):
        try:
            val = UUID(uuid_string, version=4)
        except ValueError:
            # If it's a value error, then the string
            # is not a valid hex code for a UUID.
            return False
        # If the uuid_string is a valid hex code,
        # but an invalid uuid4,
        # the UUID.__init__ will convert it to a
        # valid uuid4. This is bad for validation purposes.
        return str(val) == str(uuid_string)

    @staticmethod
    def _hash(request, widget_data):
        """
        This hash is needed to ensure date consistency.

        The provided widget data needs to be sorted in order to
        provide predictable hashing results via e.g.
        widget_data = json.dumps(provided_data, sort_keys=True)
        """
        widget_hash = sha256()
        #
        widget_hash.update(widget_data)
        return widget_hash.hexdigest()

    def store_widget(self, widget, widget_data, request):
        if self.validate_uuid4(widget):
            widget_id = widget
            self.annotations['widget_hashes'].append(
                self._hash(
                    request,
                    json.dumps(widget_data)
                )
            )
            stored_widgets = self.annotations['widgets']
            stored_widgets[widget_id] = widget_data

    def read_widget(self, widget):
        if self.validate_uuid4(widget):
            widget_id = widget
            stored_widgets = self.annotations['widgets']
            if widget_id in stored_widgets:
                return stored_widgets[widget_id]

    def delete_widget(self, widget):
        if self.validate_uuid4(widget):
            widget_id = widget
            stored_widgets = self.annotations['widgets']
            if widget_id in stored_widgets:
                del stored_widgets[widget_id]

    def widget_index(self):
        records = self.annotations.get('widgets', [])
        return len(records)

    def has_widgets(self):
        return self.widget_index() > 0

    def is_update(self, request, widget_data):
        widget_hash = self._hash(
            request,
            json.dumps(widget_data)
        )
        return widget_hash in self.annotations['widget_hashes']

    def read(self):
        return self.annotations['widgets']

    def clear(self):
        annotations = IAnnotations(self.context)
        annotations[KEY] = PersistentDict({'widget_hashes': PersistentList(),
                                           'widgets': PersistentDict()})
        self.annotations = annotations[KEY]
