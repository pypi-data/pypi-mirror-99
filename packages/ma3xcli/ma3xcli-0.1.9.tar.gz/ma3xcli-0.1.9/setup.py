# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ma3xcli']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['one = ma3xcli.one:main', 'two = ma3xcli.two:main']}

setup_kwargs = {
    'name': 'ma3xcli',
    'version': '0.1.9',
    'description': '',
    'long_description': None,
    'author': '1v1a3x',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
