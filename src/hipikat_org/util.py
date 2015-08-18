"""
Utility functions used throughout `hipikat_org`.
"""

import os

from hipikat_org import BASE_DIR


def env_setting(name, default=None, evaluate=False):
    """
    Return value of `name` from an environment variable named `DJANGO_(name)`,
    if it exists, otherwise from the contents of `(BASE_DIR)/var/env/(name)`,
    if it exists.

    If `evaluate` is `True` or a value found in the environment (or file) is
    equal to `'True'` or `'False'` (the strings), the value will be passed
    through `eval()`.

    If `default` is supplied, is not `None`, and no matching environment
    variable or file is found, its value is used for the setting, and is
    unaffected by `evaluate`.

    If all else fails, `None` is returned.
    """
    value = None
    envfile_path = os.path.join(BASE_DIR, 'var', 'env', name)

    if 'DJANGO_' + name in os.environ:
        value = os.environ['DJANGO_' + name]
    elif os.path.isfile(envfile_path):
        with open(envfile_path) as env_file:
            value = env_file.read()
    if evaluate or value in ('True', 'False'):
        value = eval(value)
    if value is None and default is not None:
        return default
    else
        return value
