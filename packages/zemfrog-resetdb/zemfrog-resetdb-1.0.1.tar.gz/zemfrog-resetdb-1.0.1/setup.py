# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zemfrog_resetdb']

package_data = \
{'': ['*']}

install_requires = \
['zemfrog>=4.0.3,<5.0.0']

setup_kwargs = {
    'name': 'zemfrog-resetdb',
    'version': '1.0.1',
    'description': 'Command to reset the database for zemfrog',
    'long_description': None,
    'author': 'aprilahijriyan',
    'author_email': 'hijriyan23@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
