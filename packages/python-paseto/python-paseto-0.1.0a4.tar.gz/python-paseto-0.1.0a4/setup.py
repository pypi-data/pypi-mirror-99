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
    'version': '0.1.0a4',
    'description': 'Platform-Agnostic Security Tokens for Python',
    'long_description': '# python-paseto\nPlatform-Agnostic Security Tokens for Python\n\n[![Build Status](https://travis-ci.org/purificant/python-paseto.svg?branch=main)](https://travis-ci.org/purificant/python-paseto)\n[![ci-workflow](https://github.com/purificant/python-paseto/actions/workflows/ci.yaml/badge.svg)](https://github.com/purificant/python-paseto/actions/workflows/ci.yaml)\n[![Coverage Status](https://coveralls.io/repos/github/purificant/python-paseto/badge.svg?branch=main)](https://coveralls.io/github/purificant/python-paseto?branch=master)\n[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/purificant/python-paseto.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/purificant/python-paseto/context:python)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n\n\n# Installation\nClone the repository, in the future a pip install will be available.\n\n[poetry](https://github.com/sdispater/poetry#installation) is used to manage project\ndependencies / build / test / publish.\n\nInstall dependencies with \n```bash\npoetry install\n```\n\nRun tests\n```bash\npytest\n```\n\nTo check code coverage run\n```bash\ncoverage run -m pytest\ncoverage report\n```\n\n# Low level API\nInitial implementation of the V2 encrypt / decrypt functions. Alpha version.\nLow level API focuses on solid, high quality, production ready primitives\nas specified directly in the [PASETO](https://tools.ietf.org/html/draft-paragon-paseto-rfc-00) \nprotocol.\n\n```python\nfrom paseto.protocol.version2 import Version2\n\nkey = b"0" * 32\nmessage = b"foo"\nfooter = b"sample_footer"\n\ntoken = Version2.encrypt(message, key, footer)\nplain_text = Version2.decrypt(token, key, footer)\n\nassert plain_text == message\n\n```\n\n# High level API\nIn the future a high level API will provide developer friendly access to low level API\nand support easy integration into other projects.\n\nCode formatting is managed by [black](https://github.com/ambv/black). To format run\n```bash\nblack .\n```',
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/purificant/python-paseto',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<3.10',
}


setup(**setup_kwargs)
