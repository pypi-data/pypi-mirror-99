# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['quick_zip',
 'quick_zip.commands',
 'quick_zip.core',
 'quick_zip.schema',
 'quick_zip.services',
 'quick_zip.utils']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.8.1,<2.0.0',
 'python-dotenv>=0.15.0,<0.16.0',
 'python-slugify>=4.0.1,<5.0.0',
 'pyzipper>=0.3.4,<0.4.0',
 'requests>=2.25.1,<3.0.0',
 'rich>=9.13.0,<10.0.0',
 'toml==0.10.2',
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['qz = quick_zip.main:main']}

setup_kwargs = {
    'name': 'quick-zip',
    'version': '0.1.5',
    'description': '',
    'long_description': None,
    'author': 'hay-kot',
    'author_email': 'hay-kot@pm.me',
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
