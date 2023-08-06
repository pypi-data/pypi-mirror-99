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
    'version': '0.1.3',
    'description': 'profile the grpc server',
    'long_description': '<h1 align="center">py-grpc-profile</h1>\n<p align="center">\nProfile the grpc server.<br>\nProvide a grpc interceptor to profile each request in the cProfile module.\n</p>\n\n<p align="center">\n    <a href="https://github.com/yhino/py-grpc-profile/actions/workflows/build.yml"><img src="https://github.com/yhino/py-grpc-profile/actions/workflows/build.yml/badge.svg" alt="build"></a>\n    <a href="https://codecov.io/gh/yhino/py-grpc-profile"><img src="https://codecov.io/gh/yhino/py-grpc-profile/branch/main/graph/badge.svg?token=KWABCP5TYT"/></a>\n</p>\n\n## Installation\n\n```shell\n$ pip install -U py-grpc-profile\n```\n\n## Example\n\nLoad the module and set the interceptors.\n\n```python\nfrom concurrent import futures\n\nimport grpc\nfrom py_grpc_profile.server.interceptor import ProfileInterceptor\n\n# ...\n\nserver = grpc.server(\n    futures.ThreadPoolExecutor(max_workers=10),\n    interceptors=[ProfileInterceptor()],\n)\n\n# ...\n```\n\nThe complete code is available in [example](https://github.com/yhino/py-grpc-profile/tree/main/example). You can find more details there.\n\n## License\n\n[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)\n',
    'author': 'Yoshiyuki HINO',
    'author_email': 'yhinoz@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/yhino/py-grpc-profile',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
