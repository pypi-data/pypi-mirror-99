# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ysdtools']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ysdtools',
    'version': '0.1.0',
    'description': 'A collection of useful python tools',
    'long_description': None,
    'author': 'ysd',
    'author_email': 'helloysd@foxmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>3.7,<4.0',
}


setup(**setup_kwargs)
