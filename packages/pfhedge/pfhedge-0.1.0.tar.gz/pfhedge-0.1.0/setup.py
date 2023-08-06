# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pfhedge',
 'pfhedge._utils',
 'pfhedge.features',
 'pfhedge.instruments',
 'pfhedge.nn',
 'pfhedge.nn.bs',
 'pfhedge.nn.modules',
 'pfhedge.stochastic']

package_data = \
{'': ['*']}

install_requires = \
['torch>=1.8.0,<2.0.0', 'tqdm>=4.59.0,<5.0.0']

setup_kwargs = {
    'name': 'pfhedge',
    'version': '0.1.0',
    'description': 'Deep Hedging in PyTorch',
    'long_description': None,
    'author': 'Shota Imaki',
    'author_email': 'shota.imaki.0801@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.13,<4.0.0',
}


setup(**setup_kwargs)
