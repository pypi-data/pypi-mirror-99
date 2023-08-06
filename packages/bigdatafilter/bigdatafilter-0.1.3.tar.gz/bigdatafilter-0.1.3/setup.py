# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bigdatafilter']

package_data = \
{'': ['*']}

install_requires = \
['tqdm>=4.59.0,<5.0.0']

setup_kwargs = {
    'name': 'bigdatafilter',
    'version': '0.1.3',
    'description': 'Easily map functions to big datasets',
    'long_description': None,
    'author': 'Andy Jackson',
    'author_email': 'amjack100@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
