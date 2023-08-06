# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['levyt']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.2,<2.0.0', 'tablib>=3.0.0,<4.0.0']

setup_kwargs = {
    'name': 'levyt',
    'version': '0.1.0',
    'description': 'Python db access made easy.',
    'long_description': None,
    'author': 'Abram Isola',
    'author_email': 'abram@isola.mn',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
