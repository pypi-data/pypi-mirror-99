# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aprsbcn']

package_data = \
{'': ['*']}

install_requires = \
['aprslib>=0.6.47,<0.7.0', 'pyowm>=3.2.0,<4.0.0', 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'aprsbcn',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Evan Pratten',
    'author_email': 'ewpratten@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
