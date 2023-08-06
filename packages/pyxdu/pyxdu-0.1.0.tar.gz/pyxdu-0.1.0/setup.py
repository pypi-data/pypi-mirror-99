# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyxdu']

package_data = \
{'': ['*']}

install_requires = \
['docopt>=0.6.2,<0.7.0']

entry_points = \
{'console_scripts': ['pyxdu = pyxdu.__main__:run']}

setup_kwargs = {
    'name': 'pyxdu',
    'version': '0.1.0',
    'description': 'Display the output of "du" in a window.',
    'long_description': None,
    'author': 'Andrey Vlasovskikh',
    'author_email': 'andrey.vlasovskikh@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
