# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ma3xcli']

package_data = \
{'': ['*']}

install_requires = \
['Pygments==2.8.1',
 'bleach==3.3.0',
 'certifi==2020.12.5',
 'chardet==4.0.0',
 'click==7.1.2',
 'colorama==0.4.4',
 'docutils==0.16',
 'idna==2.10',
 'importlib-metadata==3.7.3',
 'keyring==23.0.0',
 'packaging==20.9',
 'pkginfo==1.7.0',
 'pyparsing==2.4.7',
 'readme-renderer==29.0',
 'requests-toolbelt==0.9.1',
 'requests==2.25.1',
 'rfc3986==1.4.0',
 'six==1.15.0',
 'tqdm==4.59.0',
 'twine==3.4.0',
 'typer==0.3.2',
 'typing-extensions==3.7.4.3',
 'urllib3==1.26.4',
 'webencodings==0.5.1',
 'zipp==3.4.1']

entry_points = \
{'console_scripts': ['init-pyenv = ma3xcli.init_pyenv:main',
                     'ma3x-help = ma3xcli.ma3xhelp:main',
                     'two = ma3xcli.two:main']}

setup_kwargs = {
    'name': 'ma3xcli',
    'version': '0.1.13',
    'description': '',
    'long_description': None,
    'author': '1v1a3x',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
