# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['openglass']

package_data = \
{'': ['*']}

install_requires = \
['Sphinx>=3.4.3,<4.0.0',
 'Telethon>=1.17.5,<2.0.0',
 'recommonmark>=0.7.1,<0.8.0',
 'six>=1.15.0,<2.0.0',
 'tweepy>=3.9.0,<4.0.0']

entry_points = \
{'console_scripts': ['openglass = openglass:main']}

setup_kwargs = {
    'name': 'openglass',
    'version': '0.3.0',
    'description': 'Openglass is a tool to query various social network and search for different type of information. Openglass is in its first versions still. Please expect bugs. If you want to contribute please do get in touch.',
    'long_description': None,
    'author': 'Hiro',
    'author_email': 'hiro@torproject.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
