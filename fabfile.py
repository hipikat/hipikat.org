
from fabric.api import *
from fabtools import require
import fabtools


APP_OWNER = 'hipikat'
PYTHON_VERSION = '2.7.6'
PYTHON_TARBALL_NAME = 'Python-{version}'
PYTHON_SOURCE_URL = 'http://www.python.org/ftp/python/{version}/' + PYTHON_TARBALL_NAME + '.tgz'
DEBIAN_PACKAGES = (
    'build-essential',
    'libreadline-gplv2-dev',
    'libncursesw5-dev',
    'libssl-dev',
    'libsqlite3-dev',
    'tk-dev',
    'libgdbm-dev',
    'libc6-dev',
    'libbz2-dev',
    'libncurses5-dev',
)
PYTHON_SYSTEM_PACKAGES = (
    '',
)


#@task
#def setup_owner():
#    pass


@task
def upgrade_deb():
    """Update the APT package definitions and upgrade all pacakges."""
    fabtools.deb.update_index()
    fabtools.deb.upgrade()


@task
def install_local_python():
    python_src_dir = PYTHON_TARBALL_NAME.format(version=PYTHON_VERSION)
    require.directory('$HOME/build-python')
    with cd('$HOME/build-python'):
        run('rm -Rf ./*')
        run('wget ' + PYTHON_SOURCE_URL.format(version=PYTHON_VERSION))
        run('tar -zxf ' + python_src_dir + '.tgz')
    with cd('$HOME/build-python/' + python_src_dir):
        run('./configure')
        run('make')
        run('make install')


@task
def bootstrap_droplet():
    """Set up a fresh droplet with a package owner and a working web server."""
    #setup_owner()
    upgrade_deb()
    require.deb.packages(DEBIAN_PACKAGES)
    install_local_python()


#@task
#def setup_virtualenv():
#    # Require a Python package
#    require.directory('/env', owner='root')
#    with cd('/env'):
#        run('virtualenv
#
#    with fabtools.python.virtualenv('/home/myuser/env'):
#        require.python.package('pyramid')
#
#    # Require an email server
#    require.postfix.server('example.com')
#
#    # Require a PostgreSQL server
#    require.postgres.server()
#    require.postgres.user('myuser', 's3cr3tp4ssw0rd')
#    require.postgres.database('myappsdb', 'myuser')
#
#    # Require a supervisor process for our app
#    require.supervisor.process('myapp',
#        command='/home/myuser/env/bin/gunicorn_paster /home/myuser/env/myapp/production.ini',
#        directory='/home/myuser/env/myapp',
#        user='myuser'
#        )
#
#    # Require an nginx server proxying to our app
#    require.nginx.proxied_site('example.com',
#        docroot='/home/myuser/env/myapp/myapp/public',
#        proxy_url='http://127.0.0.1:8888'
#        )
#
#    # Setup a daily cron task
#    fabtools.cron.add_daily('maintenance', 'myuser', 'my_script.py')
#
