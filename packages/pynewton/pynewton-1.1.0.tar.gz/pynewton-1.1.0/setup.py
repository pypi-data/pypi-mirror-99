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
    'version': '1.1.0',
    'description': 'An asyncio-based wrapper for the newton-api',
    'long_description': '# PyNewton\n\nAn `asnycio`-based  wrapper for [Newton](https://newton.now.sh).\nThe Github project can be found [here.](https://github.com/aunyks/newton-api)\n\n## Installation\n```\npip install git+https://github.com/HitaloSama/pynewton\n```\n\n## Example\n\n```py\nimport asyncio\nimport pynewton\n\n# Get event loop\nloop = asyncio.get_event_loop()\n\nasync def main():\n    # Get calculation for `to_calculate`.\n    to_calculate = input("Expression: ") # 2^2+2(2)\n    \n    # Return a Result object with `operation`, `expression`\n    # and `result` as attributes.\n    result = await pynewton.simplify(to_calculate)\n    print(result)\n\nloop.run_until_complete(main())\n```\n',
    'author': 'Nils Theres',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/HitaloSama/pynewton',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
