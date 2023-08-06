# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['clickcounter', 'clickcounter.providers']

package_data = \
{'': ['*']}

install_requires = \
['lxml>=4.6.3,<5.0.0', 'requests>=2.25.1,<3.0.0']

entry_points = \
{'console_scripts': ['clickcounter = clickcounter._cli:cli']}

setup_kwargs = {
    'name': 'clickcounter',
    'version': '1.0.0',
    'description': '',
    'long_description': None,
    'author': 'Johannes Valbjorn',
    'author_email': 'johannes.valbjorn@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
