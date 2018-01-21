# Changelog

## [unreleased]

* Fixed unicode error in Python3 during pdf renaming

## [1.5.1] - 2017-10-22

* Fixed import problem with Python2

## [1.5.0] - 2017-10-14

* Use `entry_points['console_scripts']` instead of plain `scripts` in setup.py
* Moved script into `gscholar/__main__.py`
* Added `-V/--version` parameter to CLI

## [1.4.1] - 2017-10-07

* Updated README
* Updated github URL

## [1.4.0] - 2017-10-07

* Moved CLI part into separate executable and install it via setup.py
* Updated setup.py (added Metadata, etc)
* Change license from GPL2 to MIT
* Improved docstrings
* Improved logging

## [1.3.1] - 2017-10-07

* Fixed parsing of results, so queries will actually return something again
