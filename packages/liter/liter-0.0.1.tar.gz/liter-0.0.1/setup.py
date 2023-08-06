# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['liter']

package_data = \
{'': ['*']}

install_requires = \
['typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['liter = liter.console:app']}

setup_kwargs = {
    'name': 'liter',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'Jorge Morgado',
    'author_email': 'jorge.morgadov@gmail.com',
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
