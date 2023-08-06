# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tinyfilemanager']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'tinyfilemanager',
    'version': '0.2.0',
    'description': 'Python Client / SDK for tinyfilemanager',
    'long_description': '# tinyfilemanager\n\n[![tinyfilemanager - PyPi](https://img.shields.io/pypi/v/tinyfilemanager)](https://pypi.org/project/tinyfilemanager/)\n[![Supported Python versions](https://img.shields.io/pypi/pyversions/tinyfilemanager)](https://pypi.org/project/tinyfilemanager/)\n[![LICENSE](https://img.shields.io/github/license/pentatester/tinyfilemanager)](https://github.com/pentatester/tinyfilemanager/blob/main/LICENSE)\n\nPython Client / SDK for tinyfilemanager\n',
    'author': 'hexatester',
    'author_email': 'hexatester@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
