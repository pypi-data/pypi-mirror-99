# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kess']

package_data = \
{'': ['*']}

install_requires = \
['dapr-ext-fastapi>=1.0.0,<2.0.0',
 'dapr>=1.0.0,<2.0.0',
 'fastapi>=0.63.0,<0.64.0']

setup_kwargs = {
    'name': 'kess',
    'version': '0.12.0',
    'description': '',
    'long_description': None,
    'author': 'majik',
    'author_email': 'me@yamajik.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
