# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['unbound_key_control_client_api',
 'unbound_key_control_client_api.models',
 'unbound_key_control_client_api.views']

package_data = \
{'': ['*']}

install_requires = \
['base-client-api>=2.0.0,<3.0.0']

setup_kwargs = {
    'name': 'unbound-key-control-client-api',
    'version': '0.14.0',
    'description': 'Client API for Unbound Key Control',
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
