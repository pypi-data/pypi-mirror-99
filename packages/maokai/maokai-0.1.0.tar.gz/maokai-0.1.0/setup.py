# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['maokai', 'maokai.api', 'maokai.db', 'maokai.db.models']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.3.23,<2.0.0', 'pandas>=1.2.3,<2.0.0', 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'maokai',
    'version': '0.1.0',
    'description': 'wrapper for riot api and store it in sql database',
    'long_description': None,
    'author': 'Moch Rene',
    'author_email': 'moch.rene@googlemail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
