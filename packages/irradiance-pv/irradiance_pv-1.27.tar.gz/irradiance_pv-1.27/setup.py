# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['irradiance_pv']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'irradiance-pv',
    'version': '1.27',
    'description': '"Calculate in plane irradiance for a surface"',
    'long_description': '# Irradiance PV\n\nIrradiance is a simple implementation of solar position and irradiance models to calculate the incident in plane irradiance in PV Modules.\n\nThe package works its way from an horizontal global irradince, calculating solar positions, then transforming the components into a \nPlane-of-Array (POA) Irradiance, necessary for the modeling of photovoltaic energy yields.\n\n\n## Installation\n\n\n```console\n$ pip install irradiance-pv\n```\n\n## files\n\n### irradiance.py\n\nContains the main classes to create and transform the irradiance components falling into a photovoltaic system, represented by a location and a surface.\n\n### spa_sb.py\n\nContains an implementation of the solar positions algorithm developped by the Astronomical Applications Department of the US Naval Observatory.\n',
    'author': '-sergiob',
    'author_email': 'sbadilloworks@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sbadillo/irradiance-pv',
    'packages': packages,
    'package_data': package_data,
}


setup(**setup_kwargs)
