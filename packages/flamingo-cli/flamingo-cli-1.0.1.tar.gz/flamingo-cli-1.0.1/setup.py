# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['flamingo']
install_requires = \
['click', 'requests', 'tabulate']

entry_points = \
{'console_scripts': ['flamingo = flamingo.console:run']}

setup_kwargs = {
    'name': 'flamingo-cli',
    'version': '1.0.1',
    'description': 'Flamingo Command Line Interface',
    'long_description': None,
    'author': 'Joao Daher',
    'author_email': 'joao@daher.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
