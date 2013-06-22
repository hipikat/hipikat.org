#!/usr/bin/env python
import os
import sys 
from django.core.management import ManagementUtility

if __name__ == "__main__":
    os.environ["DJANGO_SETTINGS_MODULE"] = "hipikat.settings.default"
    ManagementUtility([__file__, 'make_secret_key']).execute()
