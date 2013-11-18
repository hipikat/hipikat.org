
import os
import tempfile
from textwrap import dedent
#from fabric.api import *
import fabric
from fabric.api import cd, local, run, task
from fabtools import require
import fabtools

# Project settings
from project_settings import (
    ADMINS,
    PROJECT_NAME,
    PYTHON_VERSION,
    PROJECT_GIT_URL,
)

PYTHON_SRC_DIR = 'Python-{version}'
PYTHON_SOURCE_URL = 'http://www.python.org/ftp/python/{version}/' + PYTHON_SRC_DIR + '.tgz'
EZ_SETUP_URL = 'https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py'
DEBIAN_PACKAGES = (
    # Essentials for building Python
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
    # Useful for administration
    'git',
    'screen',
    'mosh',
)
PYTHON_SYSTEM_PACKAGES = (
    'virtualenv',
    'virtualenvwrapper',
)


# TODO: Clean this up. Export it as a function? Also, clean up temp files.
@task
def create_admins():
    for admin in ADMINS:
        username = admin['username']
        user_options = ('ssh_public_keys', 'shell',)
        user_kwargs = {kwarg: admin[kwarg] for kwarg in user_options if kwarg in admin}
        if 'skeleton_dir' in admin:
            # Wrap our local skeleton directory in a tarball
            skel_basedir, skel_dirname = os.path.split(admin['skeleton_dir'])
            skelball = tempfile.mkstemp('.tgz')
            os.close(skelball[0])
            skelball_path, skelball_file = skelball[1], os.path.split(skelball[1])[1].split('.')[0]
            local('tar -zcf {outfile} -C {skel_basedir} {skel_dirname}'.format(
                outfile=skelball[1],
                skel_basedir=skel_basedir,
                skel_dirname=skel_dirname))
            # Copy the skelton directory tarball to the remote host
            require.files.directory('/tmp/' + skelball_file)
            require.files.file(os.path.join('/tmp', skelball_file, skelball_file + '.tgz'),
                               source=skelball_path)
            with cd(os.path.join('/tmp', skelball_file)):
                run('tar -zxf ' + skelball_file + '.tgz')
                run('rm ' + skelball_file + '.tgz')
            user_kwargs['skeleton_dir'] = os.path.join('/tmp', skelball_file, skel_dirname)
        require.users.user(username, **user_kwargs)
        require.users.sudoer(username)


@task
def setup_nginx():
    require.nginx.server()
    require.nginx.disabled('default')


@task
def upgrade_deb():
    """Update the APT package definitions and upgrade all packages."""
    fabtools.deb.update_index()
    fabtools.deb.upgrade()


@task
def install_local_python():
    python_src_dir = PYTHON_SRC_DIR.format(version=PYTHON_VERSION)
    require.directory('$HOME/build-python')
    with cd('$HOME/build-python'):
        run('rm -Rf ./*')
        run('wget ' + PYTHON_SOURCE_URL.format(version=PYTHON_VERSION))
        run('tar -zxf ' + python_src_dir + '.tgz')
    with cd('$HOME/build-python/' + python_src_dir):
        run('./configure')
        run('make')
        run('make install')
    run('wget {} -O - | /usr/local/bin/python'.format(EZ_SETUP_URL))
    run('/usr/local/bin/easy_install pip')

@task
def setup_local_python():
    # TODO: Work out where this should go
    for pkg in PYTHON_SYSTEM_PACKAGES:
        require.python.package(pkg, pip_cmd='/usr/local/bin/pip')
    fabric.contrib.files.append('/etc/profile', dedent("""
        # Make /env the shared virtualenv directory by default
        export WORKON_HOME=/env
        source /usr/local/bin/virtualenvwrapper.sh"""))
    run('source /usr/local/bin/virtualenvwrapper.sh')


@task
def make_virtualenv(tag=None):
    require.files.directory('/env', use_sudo=True, owner='root', mode='755')
    #with cd('/env'):
    project_dir = PROJECT_NAME + ('-' + tag if tag else '')
    run('mkvirtualenv ' + project_dir)


@task
def install_project(branch='master', tag=None):
    # TODO: Handle private repositories
    make_virtualenv(tag)
    require.files.directory('/prj', use_sudo=True, owner='root', mode='755')
    with cd('/prj'):
        dest_dir = PROJECT_NAME + ('-' + tag if tag else '')
        run('git clone git@github.com:hipikat/hipikat.org.git ' + dest_dir)
    with fabtools.python.virtualenv(dest_dir):
        run('setvirtualenvproject /env/' + dest_dir)


@task
def bootstrap_droplet():
    """Set up a fresh droplet with a package owner and a working web server."""
    create_admins()
    upgrade_deb()
    require.deb.packages(DEBIAN_PACKAGES)
    install_local_python()
    setup_local_python()
    setup_nginx()
    install_project()


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
