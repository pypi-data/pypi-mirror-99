# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stock_utilities']

package_data = \
{'': ['*']}

install_requires = \
['yfinance>=0.1.55,<0.2.0']

setup_kwargs = {
    'name': 'stock-utilities',
    'version': '0.1.3',
    'description': 'This library is a wrapper around the finance libraries in order to give out a data model different from raw pandas and be usable in production services',
    'long_description': '# stock_utilities\n\nThis repo will manage utilities for stock data and stock option\nThe idea is to fetch data from multiple sources and use them from a single point',
    'author': 'Josario Carioca',
    'author_email': '6355922-josariooo@users.noreply.gitlab.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
