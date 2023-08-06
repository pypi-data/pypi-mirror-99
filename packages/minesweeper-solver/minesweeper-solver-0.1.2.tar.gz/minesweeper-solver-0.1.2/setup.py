# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['minesweeper_solver']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.20.1,<2.0.0']

entry_points = \
{'console_scripts': ['minesweeper_solver = minesweeper_solver:main']}

setup_kwargs = {
    'name': 'minesweeper-solver',
    'version': '0.1.2',
    'description': '',
    'long_description': '# minesweeper-solver\n\n![PyPI](https://img.shields.io/pypi/v/minesweeper-solver?color=blue&style=for-the-badge)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/minesweeper-solver?color=blue&style=for-the-badge)\n![PyPI - Implementation](https://img.shields.io/pypi/implementation/minesweeper-solver?style=for-the-badge)\n\nA working example of the solver if you run `python solver.py`\n\n![1](images/1.png)\n\n![2](images/2.png)\n\n# PyPi Install\n\n```bash\npip install minesweeper-solver\nminesweeper_solver\n```\n',
    'author': 'Thomas Lee',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
