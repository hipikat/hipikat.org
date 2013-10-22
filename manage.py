#!/usr/bin/env python
import os
from os import path
import sys
import envdir

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hipikat.settings")

    # TODO: Read this stuff into the environment upon activation of the
    # virtual environment, instead.
    envdir.read(path.join(path.dirname(__file__), 'var/env'))

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
