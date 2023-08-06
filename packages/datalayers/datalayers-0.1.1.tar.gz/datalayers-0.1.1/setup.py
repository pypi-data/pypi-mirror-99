# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datalayers']

package_data = \
{'': ['*']}

install_requires = \
['jsonpointer>=2.0,<3.0']

setup_kwargs = {
    'name': 'datalayers',
    'version': '0.1.1',
    'description': 'A library to read and manipulate values within JSON files, including multiple files layered on a first-found basis',
    'long_description': None,
    'author': 'Nick Thurmes',
    'author_email': 'nthurmes@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
