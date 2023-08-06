# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['irradiance_pv']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.20.1,<2.0.0', 'pandas>=1.2.3,<2.0.0']

setup_kwargs = {
    'name': 'irradiance-pv',
    'version': '1.26',
    'description': '"Calculate in plane irradiance for a surface"',
    'long_description': '# Irradiance PV\n\nIrradiance is a simple implementation of solar position and irradiance models to calculate the incident in plane irradiance in PV Modules.\n\nThe package works its way from an horizontal global irradince, calculating solar positions, then transforming the components into a \nPlane-of-Array (POA) Irradiance, necessary for the modeling of photovoltaic energy yields.\n\n\n## Installation\n\n\n```console\n$ pip install irradiance-pv\n```\n\n## files\n\n### irradiance.py\n\nContains the main classes to create and transform the irradiance components falling into a photovoltaic system, represented by a location and a surface.\n\n### spa_sb.py\n\nContains an implementation of the solar positions algorithm developped by the Astronomical Applications Department of the US Naval Observatory.\n',
    'author': '-sergiob',
    'author_email': 'sbadilloworks@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sbadillo/irradiance-pv',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
