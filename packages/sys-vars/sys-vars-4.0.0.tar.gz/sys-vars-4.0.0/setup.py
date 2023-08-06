# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['sys_vars']
setup_kwargs = {
    'name': 'sys-vars',
    'version': '4.0.0',
    'description': 'Access system variables in your code as native Python data types.',
    'long_description': None,
    'author': 'Caleb Ely',
    'author_email': 'le717@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
