# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['aporia',
 'aporia.core',
 'aporia.core.api',
 'aporia.core.types',
 'aporia.inference',
 'aporia.inference.api',
 'aporia.pandas',
 'aporia.training',
 'aporia.training.api']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.6.2,<4.0.0',
 'certifi>=2020.12.5,<2021.0.0',
 'tenacity>=6.2.0,<7.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.5.0,<2.0.0'],
 ':python_version >= "3.5.3" and python_version < "3.6"': ['orjson>=2.0.4,<3.0.0'],
 ':python_version >= "3.6" and python_version < "4.0"': ['orjson>=3,<4'],
 'all:python_version >= "3.5.3" and python_version < "3.6"': ['numpy>=1.9.0,<2.0.0'],
 'all:python_version >= "3.5.3" and python_version < "3.6.1"': ['pandas>=0.21,<0.22'],
 'all:python_version >= "3.6" and python_version < "4.0"': ['numpy>=1.19.3,<2.0.0'],
 'all:python_version >= "3.6.1" and python_version < "4.0.0"': ['pandas>=1.1.5,<2.0.0'],
 'pandas:python_version >= "3.5.3" and python_version < "3.6"': ['numpy>=1.9.0,<2.0.0'],
 'pandas:python_version >= "3.5.3" and python_version < "3.6.1"': ['pandas>=0.21,<0.22'],
 'pandas:python_version >= "3.6" and python_version < "4.0"': ['numpy>=1.19.3,<2.0.0'],
 'pandas:python_version >= "3.6.1" and python_version < "4.0.0"': ['pandas>=1.1.5,<2.0.0'],
 'training:python_version >= "3.5.3" and python_version < "3.6"': ['numpy>=1.9.0,<2.0.0'],
 'training:python_version >= "3.5.3" and python_version < "3.6.1"': ['pandas>=0.21,<0.22'],
 'training:python_version >= "3.6" and python_version < "4.0"': ['numpy>=1.19.3,<2.0.0'],
 'training:python_version >= "3.6.1" and python_version < "4.0.0"': ['pandas>=1.1.5,<2.0.0']}

setup_kwargs = {
    'name': 'aporia',
    'version': '1.0.48',
    'description': 'Aporia SDK',
    'long_description': '# Aporia SDK',
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aporia-ai/sdk',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.5.3,<4.0.0',
}


setup(**setup_kwargs)
