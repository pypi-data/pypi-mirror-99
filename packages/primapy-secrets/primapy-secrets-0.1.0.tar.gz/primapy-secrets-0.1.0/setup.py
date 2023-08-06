# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['primapy_secrets']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'primapy-secrets',
    'version': '0.1.0',
    'description': 'Safety placeholder',
    'long_description': None,
    'author': 'AMOps team',
    'author_email': 'amops@prima.it',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
