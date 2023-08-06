# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['couplet']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'couplet',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Couplet\n\nNothing to see here yet!\n\n',
    'author': 'Tom Marks',
    'author_email': 'thomas.o.marks@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tomdottom/python-couplet',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
