# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['plmini', 'plmini.pb']

package_data = \
{'': ['*']}

install_requires = \
['grpcio>=1.36.1,<2.0.0', 'jsonschema>=3.2.0,<4.0.0', 'protobuf>=3.15.6,<4.0.0']

setup_kwargs = {
    'name': 'plmini',
    'version': '0.0.8',
    'description': 'Prototyping Lab Mini Development Library',
    'long_description': None,
    'author': 'Kotone Itaya',
    'author_email': 'kotone@sfc.keio.ac.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
