# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

from ad25.widgets.testing import IntegrationTestCase
from plone import api


class TestInstall(IntegrationTestCase):
    """Test installation of ad25.widgets into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if ad25.widgets is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('ad25.widgets'))

    def test_uninstall(self):
        """Test if ad25.widgets is cleanly uninstalled."""
        self.installer.uninstallProducts(['ad25.widgets'])
        self.assertFalse(self.installer.isProductInstalled('ad25.widgets'))

    # browserlayer.xml
    def test_browserlayer(self):
        """Test that IAd25WidgetsLayer is registered."""
        from ad25.widgets.interfaces import IAd25WidgetsLayer
        from plone.browserlayer import utils
        self.failUnless(IAd25WidgetsLayer in utils.registered_layers())
