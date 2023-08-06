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
    'version': '0.1.0.post1',
    'description': 'Python library for validation, constructing, and representing DIDs and DID Documents',
    'long_description': '# PyDID\n\n[![pypi release](https://img.shields.io/pypi/v/pydid)](https://pypi.org/project/pydid/)\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n\nPython library for representing DIDs and DID Documents.\n\n## Installation\n\nThis project will be uploaded to PyPI eventually. To install locally:\n\n```sh\n$ python -m venv env\n$ source env/bin/activate\n$ pip install poetry\n$ poetry install\n```\n\nThis will set up a python virtual environment, activate it, and install poetry,\nthe dependency manager in use for this project.\n\n## Contributing\n\nSee [CONTRIBUTING.md](CONTRIBUTING.md).\n',
    'author': 'Daniel Bluhm',
    'author_email': 'dbluhm@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dbluhm/pydid',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.9,<4.0.0',
}


setup(**setup_kwargs)
