# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['itly_plugin_snowplow']

package_data = \
{'': ['*']}

install_requires = \
['snowplow-tracker>=0.8.4,<0.9.0']

setup_kwargs = {
    'name': 'itly-plugin-snowplow',
    'version': '0.1.5',
    'description': 'Iteratively Analytics SDK - Snowplow Plugin',
    'long_description': '',
    'author': 'Iteratively',
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
