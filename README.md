# ade25.widgets

## Base package for reusable content units provided as widgets

* `Source code @ GitHub <https://github.com/ade25kk/ade25.widgets>`_
* `Releases @ PyPI <http://pypi.python.org/pypi/ade25.widgets>`_
* `Documentation @ ReadTheDocs <http://ade25widgets.readthedocs.org>`_
* `Continuous Integration @ Travis-CI <http://travis-ci.org/ade25kk/ade25.widgets>`_

## How it works

This package provides a Plone addon as an installable Python egg package.

The generated Python package holds generalized tools and utilities for managing
reusable content widgets. The widgets are registered in the plone configuration
registry and can be embedded in Plone pages.

The core target is prviding widgets that can be embedded in content layouts by the
means of layouting tools like *ade25.panelpages*.

## Installation

To install `ade25.widgets` you simply add ``ade25.widgets``
to the list of eggs in your buildout, run buildout and restart Plone.
Then, install `ade25.widgets` using the Add-ons control panel.
