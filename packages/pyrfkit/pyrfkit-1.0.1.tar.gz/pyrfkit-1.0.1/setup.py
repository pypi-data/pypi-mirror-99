# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rfkit', 'rfkit.io', 'rfkit.math']

package_data = \
{'': ['*']}

install_requires = \
['h5py>=3.2.1,<4.0.0',
 'matplotlib>=3.3.4,<4.0.0',
 'numpy>=1.20.1,<2.0.0',
 'pandas>=1.2.3,<2.0.0',
 'scikit-rf>=0.16.0,<0.17.0',
 'scipy>=1.6.1,<2.0.0']

setup_kwargs = {
    'name': 'pyrfkit',
    'version': '1.0.1',
    'description': 'Python RF Kit built on scikit-rf.',
    'long_description': None,
    'author': 'Adam Page',
    'author_email': 'adam.page@samtec.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://bitbucket.org/samteccmd/pyrfkit',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
