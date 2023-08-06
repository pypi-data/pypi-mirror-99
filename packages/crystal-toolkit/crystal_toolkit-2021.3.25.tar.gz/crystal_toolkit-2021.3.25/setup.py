# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['crystal_toolkit',
 'crystal_toolkit.apps',
 'crystal_toolkit.apps.examples',
 'crystal_toolkit.apps.examples.tests',
 'crystal_toolkit.apps.tests',
 'crystal_toolkit.components',
 'crystal_toolkit.components.transformations',
 'crystal_toolkit.core',
 'crystal_toolkit.core.tests',
 'crystal_toolkit.helpers',
 'crystal_toolkit.renderables']

package_data = \
{'': ['*'], 'crystal_toolkit.apps': ['assets/*', 'assets/fonts/*']}

install_requires = \
['crystaltoolkit-extension>=0.3.0,<0.4.0',
 'mp-pyrho>=0.0.14,<0.0.15',
 'plotly>=4.10,<5.0',
 'pydantic',
 'pymatgen>=2020.9.14,<2021.0.0',
 'scikit-image',
 'scikit-learn',
 'webcolors']

extras_require = \
{':python_version >= "3.7" and python_version < "3.8"': ['typing-extensions'],
 'fermi': ['ifermi', 'pyfftw'],
 'server': ['dash>=1.19.0,<2.0.0',
            'dash-daq',
            'gunicorn',
            'redis',
            'Flask-Caching',
            'gevent',
            'dash-mp-components>=0.2.5,<0.3.0',
            'robocrys',
            'habanero',
            'dscribe',
            'dash-extensions',
            'sentry-sdk',
            'dash-vtk>=0.0.6,<0.0.7',
            'kaleido==0.1.0']}

setup_kwargs = {
    'name': 'crystal-toolkit',
    'version': '2021.3.25',
    'description': '',
    'long_description': None,
    'author': 'Matthew Horton',
    'author_email': 'mkhorton@lbl.gov',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
