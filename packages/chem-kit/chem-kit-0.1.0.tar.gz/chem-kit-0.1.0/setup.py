# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chem_kit']

package_data = \
{'': ['*']}

install_requires = \
['ipython>=7.21.0,<8.0.0', 'numpy>=1.19.5,<2.0.0', 'pandas>=1.2.1,<2.0.0']

setup_kwargs = {
    'name': 'chem-kit',
    'version': '0.1.0',
    'description': 'A chemical toolbox based on RDKit',
    'long_description': None,
    'author': 'Yann Beauxis',
    'author_email': 'dev@yannbeauxis.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
