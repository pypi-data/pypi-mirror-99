# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['termgraphicslib']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'termgraphicslib',
    'version': '0.1.2',
    'description': 'A small graphics library for drawing lines, pixels, and tris to the screen',
    'long_description': '# termgraphicslib\ndraw epic triangles in terminal\n\n## Raycaster\nfeel free to base your project off of the provided example raycaster (raycaster.py)\n',
    'author': 'Ruthenic',
    'author_email': 'mdrakea3@tutanota.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
