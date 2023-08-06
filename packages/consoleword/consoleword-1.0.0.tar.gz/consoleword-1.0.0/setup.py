# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['consoleword']
setup_kwargs = {
    'name': 'consoleword',
    'version': '1.0.0',
    'description': 'consoleword.create()',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
