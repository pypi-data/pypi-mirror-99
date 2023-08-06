# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['woss', 'woss.contracts']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'woss.contracts',
    'version': '0.0.3',
    'description': 'Implementação de contratos em Python',
    'long_description': None,
    'author': 'Anderson Carlos Woss',
    'author_email': 'acwoss@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
