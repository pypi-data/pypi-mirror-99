# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyfinra', 'pyfinra.tests']

package_data = \
{'': ['*']}

install_requires = \
['finsymbols>=1.3.0,<2.0.0',
 'pandas>=1.2.3,<2.0.0',
 'requests>=2.25.1,<3.0.0',
 'selenium>=3.141.0,<4.0.0']

setup_kwargs = {
    'name': 'pyfinra',
    'version': '0.1.4',
    'description': 'Unoffical Python Finra Wrapper',
    'long_description': '# Unoffical Python Finra Wrapper\n\n**warning this repository is still in alpha stage** \n\n## Requirements\n- Chromium \n- Chromedriver\n\n## Installation\n\n### PIP\n\n```Bash\npip install pyfinra\n```\n\n### Build your self with Python-Poetry\n\n```Bash\npoetry install\npoetry build\n```\n\n## Example \n\n```Python\nfrom PyFinra import Ticker\n\ngme = Ticker("GME")\ntsla = Ticker("TSLA")\n\n\nprint(gme.quote(), tsla.quote())\n```\n\n## Testing\n\n```Bash\npetry run pytest\n```',
    'author': 'Sören Michaels',
    'author_email': 'soeren.michaels@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/BluhbergTerminal/PyFinra/tree/alpha',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
