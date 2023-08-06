# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aws_key_rotator']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.17.32,<2.0.0', 'coloredlogs>=15.0,<16.0']

entry_points = \
{'console_scripts': ['aws-key-rotator = aws_key_rotator.cli:main']}

setup_kwargs = {
    'name': 'aws-key-rotator',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'davido-nw',
    'author_email': 'david@nebulaworks.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
