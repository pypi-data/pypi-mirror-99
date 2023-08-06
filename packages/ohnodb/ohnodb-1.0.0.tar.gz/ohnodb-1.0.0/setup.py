# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ohnodb']

package_data = \
{'': ['*']}

install_requires = \
['schema>=0.7.4,<0.8.0']

setup_kwargs = {
    'name': 'ohnodb',
    'version': '1.0.0',
    'description': 'A very, very bad database',
    'long_description': None,
    'author': 'vcokltfre',
    'author_email': 'vcokltfre@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
