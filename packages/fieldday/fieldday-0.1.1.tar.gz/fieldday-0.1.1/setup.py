# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fieldday']

package_data = \
{'': ['*']}

install_requires = \
['Pint>=0.17,<0.18']

setup_kwargs = {
    'name': 'fieldday',
    'version': '0.1.1',
    'description': 'package for managing lists of fields for IoT',
    'long_description': None,
    'author': 'Mike Fife',
    'author_email': 'jmfife@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
