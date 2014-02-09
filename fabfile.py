import os
from contextlib import contextmanager
from fabric.api import *
from fabric.contrib.files import exists


# main configuration
env.user = 'winnuayi'
env.password = 'liverpool'
env.hosts = ['192.168.1.2', '192.168.1.3']

env.roledefs = {
    "production": ["192.168.1.3"],
    "development": ["192.168.1.2"],
}

# invert roledefs
env.invert_roledefs = {}
for i in env.roledefs:
    for j in env.roledefs[i]:
        env.invert_roledefs[j] = i

#env.hosts = ['dev@62.113.218.221']
#env.port = 13203

# misc. configuration
env.colorize_errors = True

# github
GIT_CIHEUL = 'https://github.com/ciheul/ciheul'

# root directory
env.directories = {
        "production": '~',
        "development": '~/Projects/dev'        
}


def init_directory():
    """Production and Development server have different project root 
       directory."""
    env.PROJECTS_DEV_DIR = env.directories[env.invert_roledefs[env.host_string]]
    env.BACKEND_DIR = os.path.join(env.PROJECTS_DEV_DIR, 'www')
    env.CIHEUL_DIR = os.path.join(env.BACKEND_DIR, 'ciheul')
    env.VENV_DIR = os.path.join(env.PROJECTS_DEV_DIR, 'virtualenv')
    env.VENV_CIHEUL_DIR = os.path.join(env.VENV_DIR, 'ciheul')


def setup():
    """Install all dependencies."""
    with settings(warn_only=True):
        sudo("apt-get -y install nginx")

        # check following link to login:
        # - https://help.ubuntu.com/community/PostgreSQL
        sudo("apt-get -y install postgresql")

        # GIS
        sudo("apt-get -y install gdal-bin")

        sudo("apt-get -y install supervisor")
        sudo("pip install virtualenv")


@task
@parallel
def deploy():
    """Deploy Ciheul.com web."""
    setup()
    init_directory()

    if not exists(env.VENV_CIHEUL_DIR):
        run("mkdir -p " + env.VENV_DIR)
        with cd(env.VENV_DIR):
            run("virtualenv ciheul")

    # for the first time, git clone. otherwise, ignore
    if not exists(env.CIHEUL_DIR):
        run("mkdir -p " + env.BACKEND_DIR)
        with cd(env.BACKEND_DIR):
            run('git clone ' + GIT_CIHEUL)

    with prefix("source " + os.path.join(env.VENV_CIHEUL_DIR, 'bin/activate')):
        with cd(env.CIHEUL_DIR):
            run("pip install -r requirements.txt")

    # send config file.
    put('ciheul/config.py', os.path.join(env.CIHEUL_DIR, 'ciheul/config.py'))

    # create directory for supervisor output if necessary
    sudo('mkdir -p /var/log/supervisor')

    # copy ciheul's supervisor configuration to supervisor directory
    put('supervisor_ciheul.conf', '/etc/supervisor/conf.d/ciheul.conf', use_sudo=True)
    sudo('supervisorctl reread && supervisorctl update')
    sudo('supervisorctl start ciheul')


def clean():
    """Remove anything related to Ciheul."""
    with cd(env.BACKEND_DIR):
        run("rm -rf ciheul")
    with cd(env.VENV_DIR):
        run("rm -rf ciheul")


@task
def update():
    """Update to the latest version."""
    with cd(env.CIHEUL_DIR):
        run('git stash')
        run('git pull')


@task
@roles('production')
def cmd(command):
    run(command)


@task
@parallel
def echo():
    init_directory()
    run("echo " + env.PROJECTS_DEV_DIR)
    run("echo " + env.BACKEND_DIR)
    run("echo " + env.CIHEUL_DIR)
    run("echo " + env.VENV_DIR)
    run("echo " + env.VENV_CIHEUL_DIR)
