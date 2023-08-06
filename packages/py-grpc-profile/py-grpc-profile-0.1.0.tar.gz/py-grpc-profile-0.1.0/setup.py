# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py_grpc_profile',
 'py_grpc_profile.adapter',
 'py_grpc_profile.aio',
 'py_grpc_profile.aio.server',
 'py_grpc_profile.server']

package_data = \
{'': ['*']}

install_requires = \
['grpcio>=1.34.1,<2.0.0',
 'pytest-asyncio>=0.14.0,<0.15.0',
 'pytest-grpc>=0.8.0,<0.9.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=0.12']}

setup_kwargs = {
    'name': 'py-grpc-profile',
    'version': '0.1.0',
    'description': 'profile for gRPC servers',
    'long_description': None,
    'author': 'Yoshiyuki HINO',
    'author_email': 'yhinoz@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
