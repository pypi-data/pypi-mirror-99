# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ftp_cli', 'ftp_cli.src', 'ftp_cli.src.config']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.8.1,<2.0.0', 'typer[all]>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['ftp-cli = ftp_cli.main:app']}

setup_kwargs = {
    'name': 'ftp-cli',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Vlad Galatskiy',
    'author_email': 'xfloydya@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
