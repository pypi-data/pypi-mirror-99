# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['corradin_ovp_utils', 'corradin_ovp_utils.datasets']

package_data = \
{'': ['*']}

install_requires = \
['portray>=1.5.2,<2.0.0']

setup_kwargs = {
    'name': 'corradin-ovp-utils',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'An',
    'author_email': 'hoangthienan95@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.9',
}


setup(**setup_kwargs)
