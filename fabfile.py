import os
from contextlib import contextmanager
from fabric.api import *
from fabric.contrib.files import exists


env.hosts = ['winnuayi@192.168.1.2']
env.password = 'liverpool'
#env.hosts = ['dev@62.113.218.221']
#env.port = 13203
env.colorize_errors = True

PROJECTS_DEV_DIR = '~/Projects/dev'
#PROJECTS_DEV_DIR = '~'
BACKEND_DIR = os.path.join(PROJECTS_DEV_DIR, 'www')
CIHEUL_DIR = os.path.join(BACKEND_DIR, 'ciheul')
VENV_DIR = os.path.join(PROJECTS_DEV_DIR, 'virtualenv')
VENV_CIHEUL_DIR = os.path.join(VENV_DIR, 'ciheul')

GIT_CIHEUL = 'https://github.com/ciheul/ciheul'


def setup():
    """Install all dependencies."""
    sudo("apt-get -y install nginx")
    # check following link to login:
    # - https://help.ubuntu.com/community/PostgreSQL
    sudo("apt-get -y install postgresql")
    sudo("apt-get -y install supervisor")

    sudo("pip install virtualenv")


def deploy():
    setup()

    if not exists(VENV_CIHEUL_DIR):
        run("mkdir -p " + VENV_DIR)
        with cd(VENV_DIR):
            run("virtualenv ciheul")

    # for the first time, git clone. otherwise, ignore
    if not exists(CIHEUL_DIR):
        run("mkdir -p " + BACKEND_DIR)
        with cd(BACKEND_DIR):
            run('git clone ' + GIT_CIHEUL)

    with prefix("source " + os.path.join(VENV_CIHEUL_DIR, 'bin/activate')):
        with cd(CIHEUL_DIR):
            run("pip install -r requirements.txt")

    # send config file.
    put('ciheul/config.py', os.path.join(CIHEUL_DIR, 'ciheul/config.py'))

    # create directory for supervisor output if necessary
    sudo('mkdir -p /var/log/supervisor')

    # copy ciheul's supervisor configuration to supervisor directory
    put('supervisor_ciheul.conf', '/etc/supervisor/conf.d/ciheul.conf', use_sudo=True)
    sudo('supervisorctl reread && supervisorctl update')


def clean():
    """Remove anything related to Ciheul."""
    with cd(BACKEND_DIR):
        run("rm -rf ciheul")
    with cd(VENV_DIR):
        run("rm -rf ciheul")


def update_ciheul():
    """Update to the latest version."""
    with cd(CIHEUL_DIR):
        run('git stash')
        run('git pull')
