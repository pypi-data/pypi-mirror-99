# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vektorplotter']

package_data = \
{'': ['*']}

install_requires = \
['PyQt5>=5.15.4,<6.0.0',
 'PyQtWebEngine>=5.15.4,<6.0.0',
 'numpy>=1.20.1,<2.0.0',
 'pandas>=1.2.1,<2.0.0',
 'plotly>=4.14.3,<5.0.0']

setup_kwargs = {
    'name': 'vektorplotter',
    'version': '0.1.0',
    'description': 'A simple program for basic features of analytical geometry.',
    'long_description': None,
    'author': 'Benjamin Brumm',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
