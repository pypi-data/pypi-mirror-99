# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['gh_action_docs']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0']

entry_points = \
{'console_scripts': ['gh-action-docs = gh_action_docs.app:main']}

setup_kwargs = {
    'name': 'gh-action-docs',
    'version': '1.1.2',
    'description': 'Generate markdown documentation for a Github Action',
    'long_description': None,
    'author': 'david-kirby',
    'author_email': '57732284+david-kirby@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/david-kirby/gh-action-docs',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
