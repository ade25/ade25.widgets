# -*- coding: utf-8 -*-
"""Module providing asset repository view"""
import logging

from Acquisition import aq_inner
from Products.Five import BrowserView
from plone import api
from plone.app.contenttypes.interfaces import IImage
from plone.protect.interfaces import IDisableCSRFProtection
from zope.interface import alsoProvides
from zope.lifecycleevent import modified

logger = logging.getLogger("ADE25 Widgets Repository")


class RepositoryManagerView(BrowserView):
    """ Asset repository management view """

    def __call__(self):
        return self.render()

    def render(self):
        return self.index()

    @staticmethod
    def is_authenticated():
        return not api.user.is_anonymous()

    def contained_items(self):
        items = api.content.find(
            context=self.context,
            portal_type=[
                "Image",
            ],
            sort_on="getObjPositionInParent",
        )
        return items

    def available_assets(self):
        records = []
        brains = self.contained_items()
        for brain in brains:
            records.append(
                {
                    "title": brain.Title,
                    "description": brain.Description,
                    "url": brain.getURL(),
                    "uuid": brain.UID,
                    "item_object": brain.getObject(),
                }
            )
        return records


class RepositoryManagerAssetTitleCleanup(BrowserView):
    """ Utility to rename assets to actual file title """

    def __call__(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        return self.render()

    def render(self):
        context = aq_inner(self.context)
        self._rename_assets()
        api.portal.show_message(
            message='Asset repository images renamed to actual file names',
            request=self.request
        )
        return self.request.response.redirect(context.absolute_url())

    def _rename_assets(self):
        records = api.content.find(
            context=self.context,
            portal_type=[
                "Image",
            ]
        )
        asset_idx = 0
        for record in records:
            asset_obj = record.getObject()
            # Rename records
            try:
                asset = getattr(asset_obj, 'image', None)
                if asset:
                    asset_filename = getattr(asset, 'filename', record.Title)
                    asset_obj.setTitle(asset_filename)
                    modified(asset_obj)
                    asset_obj.reindexObject(idxs='modified')
                    asset_idx += 1
            except AttributeError:
                # Handle error
                logger.info(
                    " - Could not rename image {0} with identifier {1}".format(
                        record.getId,
                        record.UID()
                    )
                )
        logger.info("Renamed {0} assets to use the actual filename as title".format(
            asset_idx
        ))
