# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dabeplech', 'dabeplech.models', 'dabeplech.parsers', 'dabeplech.parsers.kegg']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.3,<5.0.0',
 'colored>=1.4.2,<2.0.0',
 'pydantic>=1.8.1,<2.0.0',
 'requests-cache>=0.5.2,<0.6.0',
 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'dabeplech',
    'version': '0.6.0',
    'description': 'Light library to perform request to different bioinformatics APIs',
    'long_description': None,
    'author': 'Kenzo-Hugo Hillion',
    'author_email': 'hillion.kenzo@posteo.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
