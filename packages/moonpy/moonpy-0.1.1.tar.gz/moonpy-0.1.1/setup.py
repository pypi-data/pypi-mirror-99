# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['moonpy']

package_data = \
{'': ['*']}

install_requires = \
['google-api-python-client>=2.0.2,<3.0.0',
 'google-auth>=1.28.0,<2.0.0',
 'google-cloud>=0.34.0,<0.35.0',
 'numpy>=1.20.1,<2.0.0',
 'scipy>=1.6.1,<2.0.0']

setup_kwargs = {
    'name': 'moonpy',
    'version': '0.1.1',
    'description': 'Personal utils',
    'long_description': None,
    'author': 'Garrett Mooney',
    'author_email': '4910020+GarrettMooney@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
