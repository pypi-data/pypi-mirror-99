# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['realm', 'realm.cli', 'realm.cli.commands', 'realm.entities', 'realm.utils']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0.0,<8.0.0', 'toml>=0.10.2,<0.11.0']

extras_require = \
{'tasks': ['poethepoet>=0.9.0,<0.10.0']}

entry_points = \
{'console_scripts': ['realm = realm.cli.application:cli']}

setup_kwargs = {
    'name': 'realm',
    'version': '0.1.0a0',
    'description': 'A tool for managing python poetry projects',
    'long_description': None,
    'author': 'Or Levi',
    'author_email': 'orlevi128@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
