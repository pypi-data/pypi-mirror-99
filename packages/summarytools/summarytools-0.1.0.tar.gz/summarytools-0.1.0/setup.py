# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['summarytools']
setup_kwargs = {
    'name': 'summarytools',
    'version': '0.1.0',
    'description': 'This is a port of the summarytools library in R. It provides a simple exploratory data analysis report of a pandas dataframe.',
    'long_description': None,
    'author': '6chaoran',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
