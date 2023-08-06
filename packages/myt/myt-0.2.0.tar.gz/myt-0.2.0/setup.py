# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['t']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'dateparser>=1.0.0,<2.0.0', 'pytz>=2021.1,<2022.0']

entry_points = \
{'console_scripts': ['t = t.__main__:main']}

setup_kwargs = {
    'name': 'myt',
    'version': '0.2.0',
    'description': 'Time, zones',
    'long_description': None,
    'author': 'datadavev',
    'author_email': '605409+datadavev@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/datadavev/t',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
