# -*- coding: utf-8 -*-
"""Installer for the ad25.widgets package."""

from setuptools import find_packages
from setuptools import setup

import os


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

long_description = read('README.rst')

setup(
    name='ade25.widgets',
    version='1.0.0',
    description="Base package for reusable content units provided as widgets",
    long_description=long_description,
    # Get more from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
    ],
    keywords='Plone, Panelpage',
    author='Kreativkombinat GbR',
    author_email='info@kreativkombinat.de',
    url='http://pypi.python.org/pypi/ade25.widgets',
    license='BSD',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['ade25'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'jsonpickle',
        'plone.app.dexterity [relations]',
        'plone.app.relationfield',
        'plone.namedfile [blobs]',
        'setuptools',
    ],
    extras_require={
        'test': [
            'mock',
            'plone.app.testing',
            'unittest2',
        ],
        'develop': [
            'coverage',
            'flake8',
            'jarn.mkrelease',
            'plone.app.debugtoolbar',
            'plone.reload',
            'Products.Clouseau',
            'Products.DocFinderTab',
            'Products.PDBDebugMode',
            'Products.PrintingMailHost',
            'Sphinx',
            'zest.releaser',
            'zptlint',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
