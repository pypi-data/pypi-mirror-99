# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['uquake',
 'uquake.nlloc',
 'uquake.nlloc.api',
 'uquake.nlloc.api.grids',
 'uquake.nlloc.api.nlloc']

package_data = \
{'': ['*']}

install_requires = \
['Cython>=0.29.21,<0.30.0',
 'dvc>=1.11.15,<2.0.0',
 'dynaconf>=3.1.3,<4.0.0',
 'fastapi>=0.63.0,<0.64.0',
 'h5py>=3.2.1,<4.0.0',
 'ipdb>=0.13.6,<0.14.0',
 'ipython>=7.20.0,<8.0.0',
 'jedi>=0.17.2,<0.18.0',
 'matplotlib>=3.3.4,<4.0.0',
 'obspy>=1.2.2,<2.0.0',
 'phonenumbers==8.12.18',
 'pytest>=6.2.2,<7.0.0',
 'scikit-fmm>=2021.2.2,<2022.0.0',
 'setuptools_cpp>=0.1.0,<0.2.0',
 'uvicorn>=0.13.4,<0.14.0']

setup_kwargs = {
    'name': 'uquake.nlloc',
    'version': '0.2.4',
    'description': 'wrapper around A. Lomax NLLoc',
    'long_description': None,
    'author': 'jpmercier',
    'author_email': 'jpmercier01@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
