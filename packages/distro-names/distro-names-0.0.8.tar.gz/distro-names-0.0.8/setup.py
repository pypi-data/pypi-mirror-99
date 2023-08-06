# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['distro']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['distro = distro.distro:main']}

setup_kwargs = {
    'name': 'distro-names',
    'version': '0.0.8',
    'description': 'Search for the names and versions of popular OS distributions',
    'long_description': '# distro-names\n\n`A way to search OS distribution names and versions`\n\n[![Build Status](https://travis-ci.org/igorlg/distro-names.svg?branch=master)](https://travis-ci.org/igorlg/distro-names)\n\nAren\'t you tired of searching things like "Which version is Ubuntu Trusty again", or "is Debian 8 _stretch_ or _wheezy_"? Well, I am... so I wrote this small python script to match OS versions with their names and vice versa.\n\nSimply use the CLI to search like this:\n\n```bash\n$ distro trusty\nFlavour:      Ubuntu\nFull Name:    Trusty Thar\nName:         trusty\nVersions:     14.04, 14.04.6\n```\n\nor use the version:\n```bash\n$ distro debian 7\nFlavour:     Debian\nName:        wheezy\nVersions:    7\n```\n\n# Install\n\nUsing Python pip:\n\n```bash\n$ pip install distro-names\n```\n\n# Contributing\n\nPlease feel free to contribute to this humble project - you can add distro names and versions to `distro/data.py` or improve the search capabilities in `distro/distro.py`.\n\nThis is a `pure Python` implementation, so no libs are required. If you\'d like to contribute, only PyTest and make are required...\n',
    'author': 'Igor Gentil',
    'author_email': 'igorlg@amazon.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/igorlg/distro-names',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
