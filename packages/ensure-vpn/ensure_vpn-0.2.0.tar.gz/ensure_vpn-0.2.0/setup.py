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
    'version': '0.2.0',
    'description': 'A function to ensure you are connected to your favorite VPN before running your script.',
    'long_description': 'A Python function to ensure you are connected to your favorite VPN before running your script or function. It just raises an exception if you\'re not connected.\n\n## Supported VPN providers\n- Mullvad (`"mullvad"`)\n- NordVPN (`"nordvpn"`)\n- Custom IP\n\nAdd your own!\n\n## Installation\n```\npip install ensure-vpn\n```\n\n## Usage\n\nImport the function and run it as the first thing in your script:\n\n```python\nfrom ensure_vpn import ensure_vpn\n\nensure_vpn("mullvad") # raises VPNNotConnectedException if you\'re not connected.\n\n# rest of your script goes here\n```\n\nYou can also use a custom IP or subnet:\n```python\nensure_vpn("2.235.200.110") # or e.g. "2.235.200.0/24"\n```\n\nYou can also use the decorator to run the check every time before running a specific function. This is to make sure you don\'t run untrusted code if you lose your VPN connection after starting your program.\n\nNote that this can be resource intensive depending on how often you call your function so it may slow down your program considerably or get you rate-limited by the services used by this script.\n\n```python\nfrom ensure_vpn import ensure_vpn_decorator\n\n@ensure_vpn_decorator("nordvpn")\ndef do_stuff():\n    # ...\n\ndo_stuff() # VPN is checked every time you call do_stuff\n```\n',
    'author': 'Francesco Truzzi',
    'author_email': 'francesco@truzzi.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ftruzzi/ensure_vpn',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
