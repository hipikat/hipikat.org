#!/usr/bin/env python
from os import environ
from os.path import dirname, join
from sys import argv
import envdir

if __name__ == "__main__":
    # Read files from var/env/ into environment variables
    envdir.read(join(dirname(__file__), 'var/env'))

    # Default to a dumb configuration, which provides its own (insecure)
    # SECRET_KEY and uses var/db/default.db for its (Sqlite) database.
    environ.setdefault("DJANGO_SETTINGS_MODULE", "hipikat.settings")
    if "DJANGO_CONFIGURATION" not in environ or 'make_secret_key' in argv:
        environ["DJANGO_CONFIGURATION"] = "Default"

    # Load the django-configurations importer and run the command line
    from configurations.management import execute_from_command_line
    execute_from_command_line(argv)
