# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['aws_lambda_module_loader']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'aws-lambda-module-loader',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Bjoern Boschman',
    'author_email': 'bjoern.boschman@tvsquared.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
