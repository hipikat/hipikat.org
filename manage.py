#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    # TODO: Auto-bootstrap the virtual environment for this project,
    # when running directly from this `manage.py` file...

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hipikat.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
