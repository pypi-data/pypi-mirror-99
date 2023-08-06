# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fifeutil']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.2.3,<2.0.0', 'python-dateutil>=2.8.1,<3.0.0']

setup_kwargs = {
    'name': 'fifeutil',
    'version': '0.1.1',
    'description': 'Various utilities',
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
