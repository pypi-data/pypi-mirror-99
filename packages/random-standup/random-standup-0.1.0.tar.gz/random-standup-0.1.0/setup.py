# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['random_standup']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'tomlkit>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['standup = random_standup.standup:standup']}

setup_kwargs = {
    'name': 'random-standup',
    'version': '0.1.0',
    'description': 'Standup Randomizer',
    'long_description': None,
    'author': 'jidicula',
    'author_email': 'johanan@forcepush.tech',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
