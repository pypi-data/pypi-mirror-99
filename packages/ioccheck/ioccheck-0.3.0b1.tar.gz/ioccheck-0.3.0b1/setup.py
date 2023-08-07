# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ioccheck',
 'ioccheck.cli',
 'ioccheck.cli.formatters',
 'ioccheck.iocs',
 'ioccheck.services']

package_data = \
{'': ['*']}

install_requires = \
['backoff>=1.10.0,<2.0.0',
 'click>=7.1.2,<8.0.0',
 'hurry.filesize>=0.9,<0.10',
 'pyfiglet>=0.8.post1,<0.9',
 'ratelimit>=2.2.1,<3.0.0',
 'requests>=2.25.1,<3.0.0',
 'shodan>=1.25.0,<2.0.0',
 'tabulate>=0.8.9,<0.9.0',
 'termcolor>=1.1.0,<2.0.0',
 'vt-py>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['ioccheck = ioccheck.cli.cli:run']}

setup_kwargs = {
    'name': 'ioccheck',
    'version': '0.3.0b1',
    'description': 'A tool for simplifying the process of researching IOCs.',
    'long_description': None,
    'author': 'ranguli',
    'author_email': 'hello@joshmurphy.ca',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.3,<4.0.0',
}


setup(**setup_kwargs)
