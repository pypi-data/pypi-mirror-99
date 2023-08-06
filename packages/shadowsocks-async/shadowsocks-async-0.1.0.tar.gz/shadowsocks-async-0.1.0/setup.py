# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shadowsocks', 'shadowsocks.api', 'shadowsocks.mdb']

package_data = \
{'': ['*']}

install_requires = \
['bloom-filter>=1.3,<2.0',
 'cryptography>=3.3.1,<4.0.0',
 'fire>=0.3.1,<0.4.0',
 'hkdf>=0.0.3,<0.0.4',
 'httpx>=0.16.1,<0.17.0',
 'peewee>=3.14.0,<4.0.0',
 'sentry-sdk>=0.19.5,<0.20.0',
 'uvloop>=0.14.0,<0.15.0']

entry_points = \
{'console_scripts': ['asyncss = shadowsocks.server:main']}

setup_kwargs = {
    'name': 'shadowsocks-async',
    'version': '0.1.0',
    'description': 'shadowsocks built with asyncio.',
    'long_description': None,
    'author': 'laoshan-taoist',
    'author_email': '65347330+laoshan-taoist@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
