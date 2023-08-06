# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qctrl',
 'qctrl.builders',
 'qctrl.builders.custom_handlers',
 'qctrl.builders.graphql_utils',
 'qctrl.builders.graphql_utils.handlers',
 'qctrl.queries']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=19.3.0,<20.0.0',
 'cached-property>=1.5.1,<2.0.0',
 'click>=7.0,<8.0',
 'commonmark>=0.9.1,<0.10.0',
 'gql==3.0.0a4',
 'jsonschema>=3.2.0,<4.0.0',
 'numpy>=1.16.2',
 'python-dateutil>=2.8.1,<3.0.0',
 'python-forge>=18.6.0,<19.0.0',
 'pytz>=2020.1,<2021.0',
 'qctrl-commons>=5.0.0,<5.1.0',
 'requests>=2.23.0,<3.0.0',
 'tenacity>=6.0.0,<7.0.0',
 'toml>=0.10.0,<0.11.0',
 'tqdm>=4.30.0']

entry_points = \
{'console_scripts': ['qctrl = qctrl.scripts:main']}

setup_kwargs = {
    'name': 'qctrl',
    'version': '9.4.0',
    'description': 'Q-CTRL Python',
    'long_description': "# Q-CTRL Python\n\nThe Q-CTRL Python Package provides an intuitive and convenient Python interface\nto Q-CTRL's quantum control solutions for customers of Q-CTRL. To use the Q-CTRL\nPython Package, you will need a\n[BOULDER OPAL](https://q-ctrl.com/products/boulder-opal/) account.\n",
    'author': 'Q-CTRL',
    'author_email': 'support@q-ctrl.com',
    'maintainer': 'Q-CTRL',
    'maintainer_email': 'support@q-ctrl.com',
    'url': 'https://q-ctrl.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.4,<3.9',
}


setup(**setup_kwargs)
