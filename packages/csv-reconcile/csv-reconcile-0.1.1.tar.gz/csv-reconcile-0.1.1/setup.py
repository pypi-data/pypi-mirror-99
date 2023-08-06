# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['csv_reconcile', 'csv_reconcile_dice']

package_data = \
{'': ['*']}

install_requires = \
['cython>=0.29.21,<0.30.0',
 'flask-cors>=3.0.10,<4.0.0',
 'flask>=1.1.2,<2.0.0',
 'normality>=2.1.1,<3.0.0']

extras_require = \
{':python_version >= "3.7" and python_version < "3.8"': ['importlib_metadata>=3.7.3,<4.0.0']}

entry_points = \
{'console_scripts': ['csv-reconcile = csv_reconcile:main'],
 'csv_reconcile.scorers': ['dice = csv_reconcile_dice']}

setup_kwargs = {
    'name': 'csv-reconcile',
    'version': '0.1.1',
    'description': 'OpenRefine reconciliation service backed by csv resource',
    'long_description': None,
    'author': 'Douglas Mennella',
    'author_email': 'douglas.mennella@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
