# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ensure_vpn']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0', 'returns==0.15.0']

setup_kwargs = {
    'name': 'ensure-vpn',
    'version': '0.1.0',
    'description': 'A function to ensure you are connected to your favorite VPN before running your script.',
    'long_description': None,
    'author': 'Francesco Truzzi',
    'author_email': 'francesco@truzzi.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
