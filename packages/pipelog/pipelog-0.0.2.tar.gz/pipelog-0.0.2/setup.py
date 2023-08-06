# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pipelog']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.0.0,<2.0.0']

extras_require = \
{'dev': ['flake8>=3.8.4,<4.0.0',
         'flake8-annotations>=2.5.0,<3.0.0',
         'flake8-docstrings>=1.5.0,<2.0.0',
         'black>=20.8b1,<21.0',
         'bump2version>=1.0.1,<2.0.0',
         'tox>=3.21.0,<4.0.0',
         'sphinx-autobuild>=2021.3.14,<2022.0.0'],
 'docs': ['Sphinx>=3.4.3,<4.0.0',
          'furo>=2021.3.20-beta.31,<2022.0.0',
          'sphinx-copybutton>=0.3.1,<0.4.0'],
 'test': ['pytest>=6.2.1,<7.0.0', 'coverage>=5.5,<6.0']}

setup_kwargs = {
    'name': 'pipelog',
    'version': '0.0.2',
    'description': 'A python packages to make functional pandas pipelines more transparent.',
    'long_description': '=========\nPipeLog\n=========\n\n\n.. image:: https://img.shields.io/pypi/v/pipelog?style=flat-square\n        :target: https://pypi.python.org/pypi/pipelog\n\n.. image:: https://img.shields.io/travis/com/ademfr/pipelog?style=flat-square\n        :target: https://travis-ci.com/ademfr/pipelog\n\n.. image:: https://img.shields.io/readthedocs/pipelog?style=flat-square\n        :target: https://pipelog.readthedocs.io/\n        :alt: Documentation Status\n\n\npipelog tries to make functional pandas pipelines more transparent.\n\n\nFeatures\n--------\n\n* TODO\n',
    'author': 'Adem Frenk',
    'author_email': 'adem.frenk@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ademfr/pipelog',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.11,<4.0.0',
}


setup(**setup_kwargs)
