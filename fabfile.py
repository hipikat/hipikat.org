# coding=utf-8
"""
Deployment and configuration actions for hipikat.org on Digital Ocean.

Second attempt at a good fabfile, after 3b56f40e. :) Splitting all functions
likely to be common to any project into the package `scow` (following the
`tugboat` CLI for Digital Ocean).
"""

import fabric
from fabric import api
#from fabric.api import cd, local, run, task
import fabtools
from fabtools import require

# Hopefully this isn't too confusing and/or an anti-pattern(??) Certainly, Fabric
# encourages the importing of a module with tasks rather than importing the tasks
# directly, because it leads to namespaced tasks… but this looks confusing.
#from scow import tasks as scow, debug

from scow import debug
from scow import *
#(
    #init_droplet,
    #install_project,
    #debug,
    #users,
    #ubuntu,
#)

import project_settings
api.env.project = project_settings

