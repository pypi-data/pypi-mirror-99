# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jut']

package_data = \
{'': ['*'],
 'jut': ['.mypy_cache/*',
         '.mypy_cache/3.8/*',
         '.mypy_cache/3.8/_typeshed/*',
         '.mypy_cache/3.8/collections/*',
         '.mypy_cache/3.8/importlib/*',
         '.mypy_cache/3.8/jut/*',
         '.mypy_cache/3.8/os/*']}

install_requires = \
['click==7.1.2', 'nbformat==5.1.2', 'pydantic==1.8.1', 'rich==9.13.0']

setup_kwargs = {
    'name': 'jut',
    'version': '0.0.6',
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
