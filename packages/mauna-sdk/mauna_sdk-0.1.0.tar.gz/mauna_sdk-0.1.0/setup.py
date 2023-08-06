# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mauna_sdk', 'mauna_sdk.schema_config']

package_data = \
{'': ['*'], 'mauna_sdk': ['api/*', 'schema/*']}

install_requires = \
['cryptography>=3.4.6,<4.0.0', 'gql[all]==3.0.0a5', 'requests>=2.25.1,<3.0.0']

entry_points = \
{'console_scripts': ['codegen = scripts.codegen:main']}

setup_kwargs = {
    'name': 'mauna-sdk',
    'version': '0.1.0',
    'description': 'Mauna SDK',
    'long_description': None,
    'author': 'Dmitry Paramonov',
    'author_email': 'asmatic075@gmail.com',
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
