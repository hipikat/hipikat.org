#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    # TODO: Add src to python path, remove current directory?

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hipikat.settings.default")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
