# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['paseto', 'paseto.crypto', 'paseto.protocol']

package_data = \
{'': ['*']}

install_requires = \
['cython>=0.29.22,<0.30.0', 'pynacl>=1.4.0,<2.0.0', 'pysodium>=0.7.7,<0.8.0']

setup_kwargs = {
    'name': 'python-paseto',
    'version': '0.1.0a1',
    'description': 'Platform-Agnostic Security Tokens for Python',
    'long_description': None,
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<3.10',
}


setup(**setup_kwargs)
