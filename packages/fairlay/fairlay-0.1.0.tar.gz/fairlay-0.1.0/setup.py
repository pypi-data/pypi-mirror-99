# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fairlay']

package_data = \
{'': ['*']}

install_requires = \
['arrow>=1.0.3,<2.0.0',
 'httpx>=0.17.1,<0.18.0',
 'marshmallow-enum>=1.5.1,<2.0.0',
 'marshmallow>=3.10.0,<4.0.0',
 'pycryptodome>=3.10.1,<4.0.0',
 'requests>=2.25.1,<3.0.0',
 'ujson>=4.0.2,<5.0.0']

setup_kwargs = {
    'name': 'fairlay',
    'version': '0.1.0',
    'description': 'Fairlay Client for Python 3.8+',
    'long_description': None,
    'author': 'jim zhou',
    'author_email': '43537315+jimtje@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
