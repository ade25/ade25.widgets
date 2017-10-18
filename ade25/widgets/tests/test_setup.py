# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

from ade25.widgets.testing import IntegrationTestCase
from plone import api


class TestInstall(IntegrationTestCase):
    """Test installation of ade25.widgets into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if ade25.widgets is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('ade25.widgets'))

    def test_uninstall(self):
        """Test if ade25.widgets is cleanly uninstalled."""
        self.installer.uninstallProducts(['ade25.widgets'])
        self.assertFalse(self.installer.isProductInstalled('ade25.widgets'))

    # browserlayer.xml
    def test_browserlayer(self):
        """Test that Iade25WidgetsLayer is registered."""
        from ade25.widgets.interfaces import Iade25WidgetsLayer
        from plone.browserlayer import utils
        self.failUnless(Iade25WidgetsLayer in utils.registered_layers())
