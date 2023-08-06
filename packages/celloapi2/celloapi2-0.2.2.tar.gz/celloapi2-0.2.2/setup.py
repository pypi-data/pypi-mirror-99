# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['celloapi2']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'Sphinx>=3.5.3,<4.0.0',
 'black>=20.8b1,<21.0',
 'numpy>=1.20.1,<2.0.0',
 'pytest>=6.2.2,<7.0.0',
 'sphinx-rtd-theme>=0.5.1,<0.6.0']

setup_kwargs = {
    'name': 'celloapi2',
    'version': '0.2.2',
    'description': '',
    'long_description': None,
    'author': 'W.R. Jackson',
    'author_email': 'jackson@justjackson.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
