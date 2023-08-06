# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gif_writer']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.1.2,<9.0.0',
 'imageio>=2.9.0,<3.0.0',
 'numpy>=1.20.1,<2.0.0',
 'scikit-image>=0.18.1,<0.19.0',
 'tqdm>=4.59.0,<5.0.0']

setup_kwargs = {
    'name': 'gif-writer',
    'version': '0.1.0',
    'description': 'Record loop iterations of an image/several images and output to gif',
    'long_description': None,
    'author': 'Andy Jackson',
    'author_email': 'amjack100@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
