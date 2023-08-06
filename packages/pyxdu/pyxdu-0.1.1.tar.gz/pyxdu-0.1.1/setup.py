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
    'version': '0.1.1',
    'description': 'Display the output of "du" in a window.',
    'long_description': 'pyxdu\n=====\n\nPyxdu — display the output of "du" disk usage tool in a window.\n\nPyxdu is a Python port of "xdu", an X window disk usage utility. Pyxdu is a retro tool\nthat tries to follow the style of 1990s in its visual design.\n\n[![PyPI](https://img.shields.io/pypi/v/pyxdu)](https://pypi.org/project/pyxdu/)\n[![PyPI - Downloads](https://img.shields.io/pypi/dm/pyxdu)](https://pypi.org/project/pyxdu/)\n\n\nExample\n-------\n\nRun "du" to show disk usage for directory _/usr_ in megabytes, pipe the \noutput to\n"pyxdu", sort directories in numerical order:\n\n```shell\ndu -m /usr | pyxdu -n\n```\n![Dark theme][dark]\n\n\nInstallation\n------------\n\nYou can install pyxdu on Python 3.7 or newer using pip:\n\n```shell\npip install pyxdu\n```\n\n\nDescription\n-----------\n\n_Pyxdu_ is a program for displaying a graphical tree of disk space utilization as\nreported by the UNIX utility "du". The user can navigate through the tree structure and\nchange the order of the displayed information. The window is divided up into several\ncolumns, each of which is one level deeper in the directory hierarchy (from left to\nright). Boxes are drawn for each directory. The amount of vertical space occupied by\neach box is directly proportional to the amount of disk space consumed by it and all of\nits children. The name of each directory and the amount of data are displayed provided\nthat there is enough space within its box. Any space at the "bottom" of a box not\ncovered by its children to the right represents the space consumed by files _in_ that\ndirectory (as opposed to space from its children).\n\nThere are several command line options available.\n\n* `-h --help`\n    * Show help message.\n* `-n`\n    * Sort in numerical order.\n* `--dump <file>`\n    * Dump tree as JSON for debugging.\n* `-c --columns <num>`\n    * Display \\<num\\> columns \\[default: 6\\].\n* ...\n\n\nMouse Actions\n-------------\n\nThe user can move up or down the tree by clicking the left mouse on a directory box. If\nthe left most box is selected, the display will move up one level (assuming you are not\nalready at the root). If any other box is selected, it will be placed against the left\nedge of the window, and the display will be rescaled appropriately. ~~At any time the\nmiddle mouse will bring you back to the root. Clicking the right mouse will exit the\nprogram.~~\n\n\nKeystrokes\n----------\n\n* `1-9`, `0`\n    * Sets the number of columns in the display (0 = 10). \n* `/`\n    * Goto the root.\n* `q`, `Escape`\n    * Exit the program.\n* ...\n\n\n\n\n\nDevelopment\n-----------\n\nDevelopment requirements:\n\n* Python 3.7 or newer\n* [Poetry][]\n\nSet up a development environment:\n\n```shell\ngit clone https://github.com/vlasovskikh/pyxdu.git\ncd pyxdu\npoetry install\npoetry run pyxdu --help\ndu | poetry run pyxdu\n```\n\nAuthors\n-------\n\n* [Andrey Vlasovskikh][vlasovskikh]\n\n\nCredits\n-------\n\nThe original tool [xdu][] was released by Phil Dykstra on 1991-09-04. The most recent\nversion xdu 3.0 was released on 1994-06-05.\n\n\n[xdu]: https://github.com/vlasovskikh/xdu\n[poetry]: https://python-poetry.org\n[vlasovskikh]: https://pirx.ru\n[dark]: https://raw.githubusercontent.com/vlasovskikh/pyxdu/main/media/dark.png\n',
    'author': 'Andrey Vlasovskikh',
    'author_email': 'andrey.vlasovskikh@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vlasovskikh/pyxdu',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
