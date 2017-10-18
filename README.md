# ad25.widgets

## Base package for reusable content units provided as widgets

* `Source code @ GitHub <https://github.com/ade25kk/ad25.widgets>`_
* `Releases @ PyPI <http://pypi.python.org/pypi/ad25.widgets>`_
* `Documentation @ ReadTheDocs <http://ad25widgets.readthedocs.org>`_
* `Continuous Integration @ Travis-CI <http://travis-ci.org/ade25kk/ad25.widgets>`_

## How it works

This package provides a Plone addon as an installable Python egg package.

The generated Python package holds an example content type `ContentPage` which
provides a folderish version of the default **Page** document type.

The implementation is kept simple on purpose and asumes that the developer will
add further content manually.


## Installation

To install `ad25.widgets` you simply add ``ad25.widgets``
to the list of eggs in your buildout, run buildout and restart Plone.
Then, install `ad25.widgets` using the Add-ons control panel.
