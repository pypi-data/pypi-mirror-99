# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['momos', 'momos.components', 'momos.parser']

package_data = \
{'': ['*'], 'momos': ['libraries/gtest/*', 'templates/gtest/*']}

install_requires = \
['Jinja2>=2.11.2,<3.0.0',
 'case_converter>=1.0.2,<2.0.0',
 'click>=7.1.2,<8.0.0',
 'comment_parser>=1.2.3,<2.0.0',
 'lark>=0.11.1,<0.12.0',
 'lark_parser>=0.11.1,<0.12.0',
 'networkx>=2.5,<3.0',
 'pydot>=1.4.1,<2.0.0',
 'wrapt>=1.12.1,<2.0.0']

entry_points = \
{'console_scripts': ['momos = momos.cli:run']}

setup_kwargs = {
    'name': 'momos',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'codetent',
    'author_email': 'christophsw@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
