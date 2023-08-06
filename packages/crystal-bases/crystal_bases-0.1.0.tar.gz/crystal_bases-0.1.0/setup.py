# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['crystal_bases', 'crystal_bases.crystal', 'crystal_bases.young']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.3.4,<4.0.0', 'networkx>=2.5,<3.0', 'typing>=3.7.4,<4.0.0']

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.7,<0.8']}

setup_kwargs = {
    'name': 'crystal-bases',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'njuve',
    'author_email': 'ale.nnn.r@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
