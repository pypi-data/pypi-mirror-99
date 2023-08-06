# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arcane']

package_data = \
{'': ['*']}

install_requires = \
['arcane-core>=1.0.3,<2.0.0',
 'backoff>=1.10.0,<2.0.0',
 'google-api-python-client==1.7.8',
 'google-auth-httplib2==0.0.3']

setup_kwargs = {
    'name': 'arcane-mct',
    'version': '0.2.1',
    'description': 'Package description',
    'long_description': '# Arcane mct\n',
    'author': 'Arcane',
    'author_email': 'product@arcane.run',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
