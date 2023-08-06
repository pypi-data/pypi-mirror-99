# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deepee']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'deepee',
    'version': '0.1.7',
    'description': 'Fast (and cheeky) differentially private gradient-based optimisation in PyTorch',
    'long_description': '# deepee: Fast (and cheeky) differentially private gradient-based optimisation in PyTorch\n\n> From the creators of PriMIA\n\n',
    'author': 'Georgios Kaissis',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gkaissis/deepee',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
