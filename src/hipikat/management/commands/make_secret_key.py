
import random
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = "Generates a conf/SECRET_KEY file, required by Django's settings."

    def handle(self, *args, **options):
        SECRET_FILE = settings.PROJECT_ROOT.child('conf', 'secret_key.py')
        SECRET_KEY = ''.join([random.SystemRandom().choice(
            'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        ) for i in range(50)])
        secret_module = file(SECRET_FILE, 'w')
        secret_module.write("SECRET_KEY = '%s'" % (SECRET_KEY,))
        secret_module.close()
