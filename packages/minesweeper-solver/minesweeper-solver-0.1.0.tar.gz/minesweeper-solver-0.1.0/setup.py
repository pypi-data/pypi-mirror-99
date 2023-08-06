# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['minesweeper_solver']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.20.1,<2.0.0']

setup_kwargs = {
    'name': 'minesweeper-solver',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Thomas Lee',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
