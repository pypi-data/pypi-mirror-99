# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rekishikon', 'rekishikon.utils']

package_data = \
{'': ['*'], 'rekishikon': ['profiles/*']}

setup_kwargs = {
    'name': 'rekishikon',
    'version': '0.3.1',
    'description': 'A simple Language Detection Library',
    'long_description': "=================\nrekishikon\n=================\n-------------------------------------------------\nA simple, lightweight, language detection library\n-------------------------------------------------\n\nSimple Port of Nakatani Shuyo's Language Detection from Java to Python\n\n\nWith some fancy additions   \n\n.. image:: https://travis-ci.com/K-Molloy/rekishikon.svg?branch=main\n    :target: https://travis-ci.com/K-Molloy/rekishikon",
    'author': 'K-Molloy',
    'author_email': 'kieran.b.molloy@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/K-Molloy/rekishikon',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
