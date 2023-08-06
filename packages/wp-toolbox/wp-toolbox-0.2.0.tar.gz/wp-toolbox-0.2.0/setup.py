# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wp_toolbox']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'wp-toolbox',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'Thomas Zastrow',
    'author_email': 'thomas.zastrow@mpcdf.mpg.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
