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
    'version': '1.0.3',
    'description': "Create redirect url's with click monitoring from multiple providers",
    'long_description': '# ClickCounter\n\n[![Latest Version](https://img.shields.io/pypi/v/clickcounter.svg)](https://pypi.python.org/pypi/clickcounter) [![PyPI - Downloads](https://img.shields.io/pypi/dm/clickcounter?label=pypi%20downloads)](https://pypistats.org/packages/clickcounter)\n\nCreate redirect url\'s with click monitoring from multiple providers.\n\n\n### Features\n\n* Growing list of click count providers (with a common lib interface)\n* Commandline tool (CLI)\n* Simple and easy to use\n\n### Support the development ❤️\n\nYou can support the development by:\n\n1. [Buying the maintainer a coffee](https://buymeacoffee.com/sloev)\n2. [Buying some Lambdarest swag](https://www.redbubble.com/i/mug/Lambdarest-by-sloev/73793554.9Q0AD)\n\n## Install\n\nInstall from pypi:\n\n```bash\n$ pip install clickcounter\n```\n\n## Usage (module)\n\n> using the default provider (`shorturl.at`)\n\n```python\nimport os\nimport time\nimport clickcounter\n\ntrack_url = clickcounter.register_url("https://example.com")\nprint(track_url)\nfirst_count = clickcounter.get_visits(track_url)\nprint(first_count)\nclickcounter.make_visit(track_url)\ntime.sleep(2)\nsecond_count = clickcounter.get_visits(track_url)\nprint(second_count)\n\n# https://shorturl.at/iANR5\n# 0\n# 1\n```\n\n**more examples here:**\n\n* [shorturl.at example](https://github.com/sloev/clickcounter/blob/master/examples/shorturl_at.py)\n* [linkclickcounter.com example](https://github.com/sloev/clickcounter/blob/master/examples/test_linkclickcounter_com.py)\n\n## Usage (CLI)\n\n```bash\n\nusage: _cli.py [-h] [--provider PROVIDER] [--username USERNAME] [--password PASSWORD] [--url URL] [--trackurl TRACKURL]\n               command\n\npositional arguments:\n  command              valid commands: register, get, getall\n\noptional arguments:\n  -h, --help           show this help message and exit\n  --provider PROVIDER  defaults to shorturl.at\n  --username USERNAME  some providers require login\n  --password PASSWORD  some providers require login\n  --url URL            used during register\n  --trackurl TRACKURL  used during get\n```\n\n**example**: \n\n```bash\n\n$ clickcounter register --url https://example.com\nhttps://shorturl.at/wABHQ\n\n# visit the link in browser...\n# and then get click count via:\n\n$ clickcounter get --trackurl https://shorturl.at/wABHQ\n1\n```',
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
