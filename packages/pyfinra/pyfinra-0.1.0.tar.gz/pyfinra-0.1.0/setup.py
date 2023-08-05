# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyfinra']

package_data = \
{'': ['*']}

install_requires = \
['finsymbols>=1.3.0,<2.0.0',
 'pandas>=1.2.3,<2.0.0',
 'requests>=2.25.1,<3.0.0',
 'selenium>=3.141.0,<4.0.0']

setup_kwargs = {
    'name': 'pyfinra',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Sören Michaels',
    'author_email': 'soeren.michaels@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
