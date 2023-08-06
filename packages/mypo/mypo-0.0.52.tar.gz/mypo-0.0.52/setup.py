# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mypo', 'mypo.indicator', 'mypo.optimizer', 'mypo.rebalancer', 'mypo.trigger']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.20.1,<2.0.0',
 'pandas>=1.2.2,<2.0.0',
 'pymc3>=3.11.1,<4.0.0',
 'scipy>=1.6.0,<2.0.0',
 'yfinance>=0.1.55,<0.2.0']

setup_kwargs = {
    'name': 'mypo',
    'version': '0.0.52',
    'description': '',
    'long_description': '# mypo\n\ndocumatation is [here](https://sonesuke.github.io/mypo/).\n\n# Issue\n\nIssues is [here](https://github.com/sonesuke/mypo/issues)',
    'author': 'sonesuke',
    'author_email': 'iamsonesuke@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sonesuke/mypo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9.2,<4.0.0',
}


setup(**setup_kwargs)
