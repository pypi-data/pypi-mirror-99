# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['christis',
 'christis.cmd_config',
 'christis.cmd_database',
 'christis.cmd_user',
 'christis.engine',
 'christis.engine.core',
 'christis.engine.insert',
 'christis.engine.process',
 'christis.utils']

package_data = \
{'': ['*']}

install_requires = \
['ChristisMongo>=0.21,<0.22',
 'ChristisRequestor>=0.12,<0.13',
 'PyYAML>=5.3.1,<6.0.0',
 'artifacts-keyring>=0.3.1,<0.4.0',
 'keyring>=21.8.0,<22.0.0',
 'pathlib>=1.0.1,<2.0.0',
 'pymongo>=3.11.2,<4.0.0',
 'requests>=2.25.1,<3.0.0',
 'tabulate>=0.8.7,<0.9.0',
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['christis = christis.main:app']}

setup_kwargs = {
    'name': 'christis',
    'version': '0.1.0',
    'description': '',
    'long_description': 'Christis is a CLI tool that helps to manage users on the Kubernetes cluster.',
    'author': 'armin',
    'author_email': 'rmin.aminian@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
