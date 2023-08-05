# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jut']

package_data = \
{'': ['*']}

install_requires = \
['click==7.1.2', 'nbformat==5.1.2', 'pydantic==1.8.1', 'rich==9.13.0']

setup_kwargs = {
    'name': 'jut',
    'version': '0.0.7',
    'description': 'Render Jupyter Notebook in the terminal',
    'long_description': None,
    'author': 'kracekumar',
    'author_email': 'me@kracekumar.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
