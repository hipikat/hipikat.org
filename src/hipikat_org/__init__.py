"""
`hipikat_org` is the Python package for Adam Wright's personal website.
"""

from os import path


# Absolute path to the checked-out repository.
# The Python path for the project is 'BASE_DIR/src'.
#
# (/...) = /[repo]      /src         /hipikat_org             /__init__.py
BASE_DIR = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
