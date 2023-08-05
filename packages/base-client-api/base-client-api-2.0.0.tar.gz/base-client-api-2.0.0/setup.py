# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['base_client_api', 'base_client_api.models']

package_data = \
{'': ['*']}

install_requires = \
['aiodns>=2.0.0,<3.0.0',
 'aiofiles>=0.6.0,<0.7.0',
 'aiohttp>=3.7.4,<4.0.0',
 'brotlipy>=0.7.0,<0.8.0',
 'cchardet>=2.1.7,<3.0.0',
 'loguru>=0.5.3,<0.6.0',
 'pydantic>=1.8.1,<2.0.0',
 'python-rapidjson>=1.0,<2.0',
 'rich>=9.13.0,<10.0.0',
 'tenacity>=7.0.0,<8.0.0',
 'toml>=0.10.2,<0.11.0']

setup_kwargs = {
    'name': 'base-client-api',
    'version': '2.0.0',
    'description': 'Base Client API; Used to build other client APIs',
    'long_description': None,
    'author': 'Jerod Gawne',
    'author_email': 'jerodgawne@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
