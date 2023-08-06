# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['nav_dcat']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.8.1,<2.0.0', 'pytest>=6.2.1,<7.0.0']

setup_kwargs = {
    'name': 'nav-dcat',
    'version': '0.1.8',
    'description': '',
    'long_description': None,
    'author': 'NAV IT dataplattform',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
