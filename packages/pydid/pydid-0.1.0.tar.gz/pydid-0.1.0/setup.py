# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydid', 'pydid.doc']

package_data = \
{'': ['*']}

install_requires = \
['voluptuous>=0.12.1,<0.13.0']

setup_kwargs = {
    'name': 'pydid',
    'version': '0.1.0',
    'description': 'Python library for validation, constructing, and representing DIDs and DID Documents',
    'long_description': None,
    'author': 'Daniel Bluhm',
    'author_email': 'dbluhm@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.9,<4.0.0',
}


setup(**setup_kwargs)
