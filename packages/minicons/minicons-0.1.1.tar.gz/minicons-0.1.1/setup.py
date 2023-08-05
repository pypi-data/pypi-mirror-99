# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['minicons']

package_data = \
{'': ['*']}

install_requires = \
['torch>=1.8.0,<2.0.0', 'transformers>=4.4.1,<5.0.0']

setup_kwargs = {
    'name': 'minicons',
    'version': '0.1.1',
    'description': 'A package of useful functions to analyze transformer based language models.',
    'long_description': None,
    'author': 'Kanishka Misra',
    'author_email': 'kmisra@purdue.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
