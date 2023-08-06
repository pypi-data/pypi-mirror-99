# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hypeme']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'hypeme',
    'version': '0.1.0',
    'description': 'hype yourself up!',
    'long_description': None,
    'author': 'sneakers-the-rat',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.3',
}


setup(**setup_kwargs)
