pyxdu
=====

Pyxdu — display the output of "du" disk usage tool in a window.

Pyxdu is a Python port of "xdu", an X window disk usage utility. Pyxdu is a retro tool
that tries to follow the style of 1990s in its visual design.

[![PyPI](https://img.shields.io/pypi/v/pyxdu)](https://pypi.org/project/pyxdu/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/pyxdu)](https://pypi.org/project/pyxdu/)


Example
-------

Run "du" to show disk usage for directory _/usr_ in megabytes, pipe the 
output to
"pyxdu", sort directories in numerical order:

```shell
du -m /usr | pyxdu -n
```
![Dark theme][dark]


Installation
------------

You can install pyxdu on Python 3.7 or newer using pip:

```shell
pip install pyxdu
```


Description
-----------

_Pyxdu_ is a program for displaying a graphical tree of disk space utilization as
reported by the UNIX utility "du". The user can navigate through the tree structure and
change the order of the displayed information. The window is divided up into several
columns, each of which is one level deeper in the directory hierarchy (from left to
right). Boxes are drawn for each directory. The amount of vertical space occupied by
each box is directly proportional to the amount of disk space consumed by it and all of
its children. The name of each directory and the amount of data are displayed provided
that there is enough space within its box. Any space at the "bottom" of a box not
covered by its children to the right represents the space consumed by files _in_ that
directory (as opposed to space from its children).

There are several command line options available.

* `-h --help`
    * Show help message.
* `-n`
    * Sort in numerical order.
* `--dump <file>`
    * Dump tree as JSON for debugging.
* `-c --columns <num>`
    * Display \<num\> columns \[default: 6\].
* ...


Mouse Actions
-------------

The user can move up or down the tree by clicking the left mouse on a directory box. If
the left most box is selected, the display will move up one level (assuming you are not
already at the root). If any other box is selected, it will be placed against the left
edge of the window, and the display will be rescaled appropriately. ~~At any time the
middle mouse will bring you back to the root. Clicking the right mouse will exit the
program.~~


Keystrokes
----------

* `1-9`, `0`
    * Sets the number of columns in the display (0 = 10). 
* `/`
    * Goto the root.
* `q`, `Escape`
    * Exit the program.
* ...





Development
-----------

Development requirements:

* Python 3.7 or newer
* [Poetry][]

Set up a development environment:

```shell
git clone https://github.com/vlasovskikh/pyxdu.git
cd pyxdu
poetry install
poetry run pyxdu --help
du | poetry run pyxdu
```

Authors
-------

* [Andrey Vlasovskikh][vlasovskikh]


Credits
-------

The original tool [xdu][] was released by Phil Dykstra on 1991-09-04. The most recent
version xdu 3.0 was released on 1994-06-05.


[xdu]: https://github.com/vlasovskikh/xdu
[poetry]: https://python-poetry.org
[vlasovskikh]: https://pirx.ru
[dark]: https://raw.githubusercontent.com/vlasovskikh/pyxdu/main/media/dark.png
