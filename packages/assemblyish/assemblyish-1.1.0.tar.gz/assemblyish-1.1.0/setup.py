# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['assemblyish']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'assemblyish',
    'version': '1.1.0',
    'description': 'A very simple assembly-like language, made using Python',
    'long_description': None,
    'author': 'vcokltfre',
    'author_email': 'vcokltfre@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
