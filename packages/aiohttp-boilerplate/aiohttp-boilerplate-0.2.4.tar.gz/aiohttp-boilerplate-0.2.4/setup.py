# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiohttp_boilerplate',
 'aiohttp_boilerplate.auth',
 'aiohttp_boilerplate.bootstrap',
 'aiohttp_boilerplate.config',
 'aiohttp_boilerplate.dbpool',
 'aiohttp_boilerplate.logging',
 'aiohttp_boilerplate.middleware',
 'aiohttp_boilerplate.models',
 'aiohttp_boilerplate.schemas',
 'aiohttp_boilerplate.sql',
 'aiohttp_boilerplate.test_utils',
 'aiohttp_boilerplate.views']

package_data = \
{'': ['*']}

install_requires = \
['PyJWT==1.7.1',
 'aiocache==0.11.1',
 'aiohttp==3.6.2',
 'asyncpg==0.20.1',
 'marshmallow==2.19.5',
 'python-json-logger==2.0.1',
 'ujson==1.35',
 'uvloop==0.14.0']

setup_kwargs = {
    'name': 'aiohttp-boilerplate',
    'version': '0.2.4',
    'description': '',
    'long_description': None,
    'author': 'Vladyslav Tarasenko',
    'author_email': 'vladka@webdevelop.pro',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
