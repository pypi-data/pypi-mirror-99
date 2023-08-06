# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['s3_client_lib']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.14.18,<2.0.0', 'requests==2.24.0']

setup_kwargs = {
    'name': 's3-client-lib',
    'version': '0.1.4',
    'description': 'S3 client lib',
    'long_description': None,
    'author': 'Radim Spigel',
    'author_email': 'spigel@cesnet.cz',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
