# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyaprsfi', 'pyaprsfi.exceptions']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'pyaprsfi',
    'version': '1.0.0',
    'description': 'An aprs.fi API client for Python',
    'long_description': None,
    'author': 'Evan Pratten',
    'author_email': 'ewpratten@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
