"""
Run a development server and all build processess.
"""
from optparse import make_option
import os
import subprocess
from django.core.management.commands import runserver
from django.conf import settings


def watch_sass():
    subprocess.call(
        'bundle exec compass watch &',
        cwd=os.path.join(settings.BASE_DIR, 'src', 'styles'),
        shell=True,
    )


# WISHLIST: Check out django-pipeline instead? :P
# TODO: Move build process runners to something in scripts/?
# TODO: Fix this! It currently looks like subclassing runserver.Command
# at all will result in broken sockets and missing statics. :c
class Command(runserver.Command):
    help = "Runs build programs for the project in the background,"
    "and a Django runserver instance in the foreground. The runserver"
    "--traceback option defaults to true."

    option_list = runserver.Command.option_list + (
        make_option('--no-traceback', action='store_true',
                    help="Do not print traceback on exception."),
    )

    def handle(self, *args, **options):
        # Check this is the main thread and not one spawned by autoreload
        #if not os.environ.get('RUN_MAIN', False):
        #    watch_sass()
        #if not options['no_traceback']:
        #    options['traceback'] = True
        super(Command, self).handle(*args, **options)
