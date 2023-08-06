# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sym',
 'sym.sdk',
 'sym.sdk._internal',
 'sym.sdk._internal.events',
 'sym.sdk._internal.integrations',
 'sym.sdk._internal.user',
 'sym.sdk.integrations',
 'sym.sdk.integrations.dangerous',
 'sym.sdk.tests',
 'sym.sdk.tests.integrations',
 'sym.sdk.tests.integrations.handlers',
 'sym.sdk.tests.static']

package_data = \
{'': ['*']}

install_requires = \
['bcrypt>=3.2,<4.0',
 'pdpyras>=4.1.2,<5.0.0',
 'pydantic>=1.7.3,<2.0.0',
 'requests>=2.25.1,<3.0.0',
 'semver>=2.13.0,<3.0.0',
 'structlog>=20.1,<21.0',
 'virtualenv==20.4.1']

setup_kwargs = {
    'name': 'sym-sdk',
    'version': '0.0.1',
    'description': "Sym's Python SDK",
    'long_description': "# Welcome to Sym's Python SDK!\n\nhttps://sdk.docs.symops.com/\n",
    'author': 'Sym Engineering',
    'author_email': 'pypi@symops.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://sdk.docs.symops.com/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.6,<4.0.0',
}


setup(**setup_kwargs)
