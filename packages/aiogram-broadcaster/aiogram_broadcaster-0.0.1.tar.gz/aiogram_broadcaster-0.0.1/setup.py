# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiogram_broadcaster']

package_data = \
{'': ['*']}

install_requires = \
['aiogram>=2.12,<3.0']

setup_kwargs = {
    'name': 'aiogram-broadcaster',
    'version': '0.0.1',
    'description': 'Simple and lightweight library based on aiogram for creating telegram mailings',
    'long_description': '# aiogram_broadcaster\nSimple and lightweight library based on aiogram for creating telegram mailings\n',
    'author': 'F0rzend',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fonco/aiogram-broadcaster/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
