
import random
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = "Generates a secret key in %s" % settings.SECRET_KEY_FILE

    def handle(self, *args, **options):
        secret_key = ''.join([random.SystemRandom().choice(
            'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        ) for i in range(50)])
        with open(settings.SECRET_KEY_FILE, 'w') as f:
            f.write(secret_key)
