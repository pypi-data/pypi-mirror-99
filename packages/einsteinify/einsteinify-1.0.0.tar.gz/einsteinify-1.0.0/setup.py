# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['einsteinify']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'einsteinify',
    'version': '1.0.0',
    'description': 'A package that transforms every C #include absolute path to a given directory to a relative path to the .c or .h file',
    'long_description': '# einsteinify\nA pip moudle that transforms every C #include absolute path to a given directory to a relative path to the .c or .h file\n',
    'author': 'Eugenio Berretta',
    'author_email': 'euberdeveloper@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/euberdeveloper/einsteinify',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
