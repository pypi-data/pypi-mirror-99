# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['airsupply']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=20.2.0',
 'boto3>=1.14.0',
 'click>=7.0',
 'jinja2>=2.10.3',
 'pyaxmlparser>=0.3.24']

entry_points = \
{'console_scripts': ['airsupply = airsupply.cli:main']}

setup_kwargs = {
    'name': 'airsupply',
    'version': '0.2.8',
    'description': 'Manage OTA distribution for IPA and APK files.',
    'long_description': None,
    'author': 'Michael Merickel',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
