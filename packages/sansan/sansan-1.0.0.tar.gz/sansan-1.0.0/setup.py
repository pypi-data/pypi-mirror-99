# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['sansan']
setup_kwargs = {
    'name': 'sansan',
    'version': '1.0.0',
    'description': 'a = San() print(a.san1(123))',
    'long_description': None,
    'author': 'Fazilbek',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
