# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['olas']

package_data = \
{'': ['*']}

install_requires = \
['Cartopy>=0.18.0,<0.19.0',
 'dask[complete]>=2021.3.0,<2022.0.0',
 'matplotlib>=3.3.4,<4.0.0',
 'netCDF4>=1.5.6,<2.0.0',
 'numpy>=1.20.1,<2.0.0',
 'scipy>=1.6.1,<2.0.0',
 'xarray>=0.17.0,<0.18.0']

setup_kwargs = {
    'name': 'olas',
    'version': '0.1.4',
    'description': 'Library with wave tools like ESTELA',
    'long_description': 'olas\n===========================\n|pypi package version| |conda-forge version| |python supported shield|\n\nLibrary with wave tools like ESTELA\n\nInstallation\n------------\n:with conda: conda install -c conda-forge olas\n:with pip: pip install olas # requires having cartopy (can be installed with conda install -c conda-forge cartopy)\n\n.. |python supported shield| image:: https://img.shields.io/pypi/pyversions/olas.svg\n   :target: https://pypi.python.org/pypi/olas\n.. |conda-forge version| image:: https://img.shields.io/conda/vn/conda-forge/olas.svg\n   :target: https://anaconda.org/conda-forge/olas\n.. |pypi package version| image:: https://img.shields.io/pypi/v/olas.svg\n   :target: https://pypi.python.org/pypi/olas\n\n',
    'author': 'jorge.perez',
    'author_email': 'j.perez@metocean.co.nz',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jorgeperezg/olas',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
