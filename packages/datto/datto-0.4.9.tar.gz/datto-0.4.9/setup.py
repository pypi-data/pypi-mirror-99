# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datto', 'datto.data']

package_data = \
{'': ['*']}

install_requires = \
['black>=19.10b0,<20.0',
 'catboost>=0.24.1,<0.25.0',
 'gensim>=3.8.3,<4.0.0',
 'hypothesis>=5.35.2,<6.0.0',
 'ipython>=7.8,<8.0',
 'lightgbm>=3.0.0,<4.0.0',
 'lime>=0.2.0,<0.3.0',
 'notebook>=6.0.3,<7.0.0',
 'pandas>=1.0.4,<2.0.0',
 'psycopg2-binary>=2.8.5,<3.0.0',
 'pylint>=2.5.0,<3.0.0',
 'pytest>=5.2,<6.0',
 'python-json-logger>=0.1.11,<0.2.0',
 's3fs>=0.4.2,<0.5.0',
 'shap>=0.36.0,<0.37.0',
 'sklearn>=0.0,<0.1',
 'spacy>=2.2.4,<3.0.0',
 'sphinx-rtd-theme>=0.5.0,<0.6.0',
 'sphinx>=3.2.1,<4.0.0',
 'xgboost>=1.1.1,<2.0.0']

setup_kwargs = {
    'name': 'datto',
    'version': '0.4.9',
    'description': 'Data Tools (Dat To)',
    'long_description': None,
    'author': 'kristiewirth',
    'author_email': 'kristie.ann.wirth@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
