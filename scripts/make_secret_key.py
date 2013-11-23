#!/usr/bin/env python
import os
import sys 
from django.core.management import ManagementUtility

import random
from django.core.management.base import BaseCommand
from django.conf import settings


SECRET_KEY_LENGTH = 50
SECRET_KEY_CHARS = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'


def secret_key_string():
    return ''.join(
        [random.SystemRandom().choice(SECRET_KEY_CHARS)
        for _ in range(SECRET_KEY_LENGTH)])


if __name__ == "__main__":
    print(secret_key_string()),
