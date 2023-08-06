# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pynewton']

package_data = \
{'': ['*']}

install_requires = \
['httpx[http2]>=0.17.1,<0.18.0']

setup_kwargs = {
    'name': 'pynewton',
    'version': '1.0.8',
    'description': 'An asyncio-based wrapper for the newton-api',
    'long_description': None,
    'author': 'Nils Theres',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
