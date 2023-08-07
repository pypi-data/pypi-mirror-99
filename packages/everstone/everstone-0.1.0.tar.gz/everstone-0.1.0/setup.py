# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['everstone', 'everstone.sql']

package_data = \
{'': ['*']}

install_requires = \
['asyncpg>=0.22.0,<0.23.0', 'sqlparse>=0.4.1,<0.5.0']

setup_kwargs = {
    'name': 'everstone',
    'version': '0.1.0',
    'description': 'Simple Database Query Generator',
    'long_description': None,
    'author': 'scragly',
    'author_email': '29337040+scragly@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
