# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pickfun']

package_data = \
{'': ['*']}

install_requires = \
['humanize>=3.3.0,<4.0.0']

setup_kwargs = {
    'name': 'pickfun',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Will Holtz',
    'author_email': 'wholtz@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
