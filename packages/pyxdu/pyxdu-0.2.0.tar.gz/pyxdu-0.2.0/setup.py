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
    'version': '0.2.0',
    'description': 'Display the output of "du" in a window.',
    'long_description': 'pyxdu\n=====\n\nPyxdu — display the output of "du" disk usage tool in a window.\n\nPyxdu is a Python port of "xdu", an X window disk usage utility. Pyxdu is a retro tool\nthat tries to follow the style of 1990s in its visual design.\n\n[![PyPI](https://img.shields.io/pypi/v/pyxdu)](https://pypi.org/project/pyxdu/)\n[![PyPI - Downloads](https://img.shields.io/pypi/dm/pyxdu)](https://pypi.org/project/pyxdu/)\n\n\nExample\n-------\n\nRun "du" to show disk usage for directory _/usr_ in megabytes, pipe the output to\n"pyxdu", sort directories in numerical order:\n\n```shell\ndu -m /usr | pyxdu -n\n```\n\n![Dark theme][dark]\n\n\nInstallation\n------------\n\nYou can install pyxdu on Python 3.7 or newer using pip:\n\n```shell\npip install pyxdu\n```\n\n\nDescription\n-----------\n\n_Pyxdu_ is a program for displaying a graphical tree of disk space utilization as\nreported by the UNIX utility "du". The user can navigate through the tree structure and\nchange the order of the displayed information. The window is divided up into several\ncolumns, each of which is one level deeper in the directory hierarchy (from left to\nright). Boxes are drawn for each directory. The amount of vertical space occupied by\neach box is directly proportional to the amount of disk space consumed by it and all of\nits children. The name of each directory and the amount of data are displayed provided\nthat there is enough space within its box. Any space at the "bottom" of a box not\ncovered by its children to the right represents the space consumed by files _in_ that\ndirectory (as opposed to space from its children).\n\nThere are several command line options available.\n\n* `-h --help`\n  * Show help message.\n* `-s`\n  * ~~Don\'t display sizes.~~ (not supported yet)\n* `-a`\n  * Sort in alphabetical order.\n* `-n`\n  * Sort in numerical order (the largest first).\n* `-r`\n  * Reverse sense of sort (e.g. `-rn` means the smallest first).\n* `-c <num>`\n  * Display `<num>` columns \\[default: 6\\].\n* `--foreground <color>`\n  * ~~Determines the color of the text and lines.~~ (not supported yet)\n* `--background <color>`\n  * ~~Determines the color of the background.~~ (not supported yet)\n* `--dump <file>`\n  * Dump tree as JSON for debugging.\n\nMouse Actions\n-------------\n\nThe user can move up or down the tree by clicking the left mouse on a directory box. If\nthe left most box is selected, the display will move up one level (assuming you are not\nalready at the root). If any other box is selected, it will be placed against the left\nedge of the window, and the display will be rescaled appropriately. ~~At any time the\nmiddle mouse will bring you back to the root. Clicking the right mouse will exit the\nprogram.~~ (not supported yet)\n\n\nKeystrokes\n----------\n\n* `1-9`, `0`\n  * Sets the number of columns in the display (0 = 10).\n* `a`\n  * Alphabetical sort.\n* `n`\n  * Numerical sort (the largest first).\n* `f`\n  * First-in-first-out sort (this is the order the data was read into the program).\n* `l`\n  * Last-in-first-out sort.\n* `r`\n  * Reverse sense of sort.\n* `s`\n  * ~~Toggle size display.~~ (not supported yet)\n* `h`\n  * ~~Display a popup help window.~~ (not supported yet)\n* `i`\n  * ~~Display information about the current root node to standard out. The first line\n    shows the path within the tree, the total size from this node on down, and the\n    percentage that total represents of all the data given to xdu. Subsequent lines show\n    the size and name information for all children of this node in the order they are\n    currently sorted in. This allows tiny directories to be seen that otherwise could\n    not be labeled on the display, and also allows for cutting and pasting of the\n    information.~~ (not supported yet)\n* `/`\n  * Goto the root.\n* `q`, `Escape`\n  * Exit the program.\n\n\nDevelopment\n-----------\n\nDevelopment requirements:\n\n* Python 3.7 or newer\n* [Poetry][]\n\nSet up a development environment:\n\n```shell\ngit clone https://github.com/vlasovskikh/pyxdu.git\ncd pyxdu\npoetry install\npoetry run pyxdu --help\ndu | poetry run pyxdu\n```\n\n\nAuthors\n-------\n\n* [Andrey Vlasovskikh][vlasovskikh]\n\n\nCredits\n-------\n\nThe original tool [xdu][] was released by Phil Dykstra on 1991-09-04. The most recent\nversion xdu 3.0 was released on 1994-06-05.\n\n\n[xdu]: https://github.com/vlasovskikh/xdu\n[poetry]: https://python-poetry.org\n[vlasovskikh]: https://pirx.ru\n[dark]: https://raw.githubusercontent.com/vlasovskikh/pyxdu/main/media/dark.png\n',
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
