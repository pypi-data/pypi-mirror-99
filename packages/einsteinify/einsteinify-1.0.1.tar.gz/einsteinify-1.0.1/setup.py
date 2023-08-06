# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['einsteinify']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'einsteinify',
    'version': '1.0.1',
    'description': 'A package that transforms every C #include absolute path to a given directory to a relative path to the .c or .h file',
    'long_description': '# einsteinify\nA pip moudle that transforms every C #include absolute path to a given directory to a relative path to the .c or .h file\n\n## Install\n\nYou can install einsteinify with pip:\n\n```sh\n$ pip install einsteinify\n```\n\n## Project purpose\n\nIt may happen that you have a folder with `.c` and `.h` files where some the `#include "*.h"` are **global paths** to respect to the root folder. This module makes them **relative paths** to the root folder.\n\n## Usage\n\n```python\nfrom einsteinify import einsteinify\n\nPATH = \'path/to/root/folder\'\n\neinsteinify(PATH)\n```\n\n## Result\n\nSuppose that you have a directory like this:\n\n```\nroot\n ├── main.h\n ├── other.h\n ├─> services\n │   └── services.h\n └─> utils\n     └── utils.h\n```\n\nWhere initially:\n\n**main.h**\n\n```c\n#include "root/other.h"\n#include "root/services/services.h"\n```\n\n**other.h**\n\n```c\n#include "root/utils/utils.h"\n```\n\n**utils.h**\n\n```c\n#include "root/other.h"\n#include "root/services/services.h"\n```\n\nAfter running **einsteinify** the includes would be:\n\n**main.h**\n\n```c\n#include "./other.h"\n#include "./services/services.h"\n```\n\n**other.h**\n\n```c\n#include "./utils/utils.h"\n```\n\n**utils.h**\n\n```c\n#include "./other.h"\n#include "../services.h"\n```\n',
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
