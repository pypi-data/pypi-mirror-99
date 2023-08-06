# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['termgraphicslib']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'termgraphicslib',
    'version': '0.1.0.1',
    'description': 'A small graphics library for drawing lines, pixels, and tris to the screen',
    'long_description': "just include canvas.py in your project and install the requirements in the requirements.txt, all of the other stuff is for the example raycaster (that doesn't currently work)\nas always, docs coming Soon:tm:\n",
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
