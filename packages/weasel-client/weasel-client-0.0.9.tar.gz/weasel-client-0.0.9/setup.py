# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['weasel_client',
 'weasel_client.raw_results',
 'weasel_client.resources',
 'weasel_client.scripts']

package_data = \
{'': ['*']}

install_requires = \
['python-dateutil>=2.8.1,<3.0.0', 'requests>=2.25.1,<3.0.0']

entry_points = \
{'console_scripts': ['weasel_result_fetcher = '
                     'weasel_client.scripts.raw_result_fetcher:main']}

setup_kwargs = {
    'name': 'weasel-client',
    'version': '0.0.9',
    'description': '`weasel-client` is a python library to access the `weasel-api`.',
    'long_description': None,
    'author': 'Lennart Haas',
    'author_email': 'haasl@cs.uni-bonn.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
