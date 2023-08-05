# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jean_engdata', 'jean_engdata.math']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'jean-engdata',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'jeangavb',
    'author_email': 'jean.martins@gavb.com.br',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
