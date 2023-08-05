# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hashicorp_vault_client_api',
 'hashicorp_vault_client_api.models',
 'hashicorp_vault_client_api.views']

package_data = \
{'': ['*']}

install_requires = \
['base-client-api>=2.0.0,<3.0.0']

setup_kwargs = {
    'name': 'hashicorp-vault-client-api',
    'version': '0.2.0',
    'description': 'HashiCorp Vault Client API',
    'long_description': None,
    'author': 'Jerod Gawne',
    'author_email': 'jerodgawne@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9.0,<4.0.0',
}


setup(**setup_kwargs)
