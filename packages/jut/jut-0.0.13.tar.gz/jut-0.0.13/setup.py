# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jut']

package_data = \
{'': ['*']}

install_requires = \
['click==7.1.2', 'nbformat==5.1.2', 'pydantic==1.8.1', 'rich==9.13.0']

entry_points = \
{'console_scripts': ['jut = jut.cli:main']}

setup_kwargs = {
    'name': 'jut',
    'version': '0.0.13',
    'description': 'Render Jupyter Notebook in the terminal',
    'long_description': '`jut - JUpyter notebook Terminal viewer`.\n\nThe command line tool view the IPython/Jupyter notebook in the terminal.\n\n### Install\n\n`pip install jut`\n\n### Usage\n\n``` shell\n$jut --help\nUsage: jut [OPTIONS]\n\nOptions:\n  -u, --url TEXT             Render the ipynb file from the URL\n  -i, --input-file FILENAME  File from the local file-system\n  -h, --head INTEGER         Display first n cells. Default is 10\n  -t, --tail INTEGER         Display last n cells\n  -p, --single-page          Should the result be in a single page?\n  -f, --full-display         Should all the contents in the file displayed?\n  --help                     Show this message and exit.\n\n```\n\n### ASCIICinema Demo\n\n[![asciicast](https://asciinema.org/a/400349.svg)](https://asciinema.org/a/400349)\n\n\n### Display first five cells\n\n![jut-head-example](https://raw.githubusercontent.com/kracekumar/jut/main/images/jut-head.png)\n\n### Display last five cells\n\n![jut-tail-example](https://raw.githubusercontent.com/kracekumar/jut/main/images/jut-tail.png)\n\n### Download the file and display first five cells\n\n![jut-download-url](https://raw.githubusercontent.com/kracekumar/jut/main/images/jut-download.png)\n',
    'author': 'kracekumar',
    'author_email': 'me@kracekumar.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kracekumar/jut/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
