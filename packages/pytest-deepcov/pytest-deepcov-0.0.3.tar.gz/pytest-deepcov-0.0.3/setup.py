# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['deepcov']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'coverage>=5.5,<6.0',
 'junitparser>=2.0.0,<3.0.0',
 'pydantic>=1.8.1,<2.0.0',
 'pytest-cov>=2.11.1,<3.0.0',
 'rich>=9.13.0,<10.0.0',
 'timeago>=1.0.15,<2.0.0']

entry_points = \
{'console_scripts': ['deepcov = deepcov.cli:run'],
 'pytest11': ['deepcov = deepcov.pytest_plugin']}

setup_kwargs = {
    'name': 'pytest-deepcov',
    'version': '0.0.3',
    'description': 'deepcov',
    'long_description': None,
    'author': 'alex-treebeard',
    'author_email': 'alex@treebeard.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/treebeardtech/deepcov',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
