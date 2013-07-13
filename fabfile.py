from fabric.api import local
import pip
 
def upgrade_packages():
    for dist in pip.get_installed_distributions():
        local("pip install --upgrade {0}".format(dist.project_name))

def covered():
    local("coverage run --source=src manage.py test hipikat revkom")
    local("coverage report")
