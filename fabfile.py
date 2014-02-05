import os
from contextlib import contextmanager
from fabric.api import *
from fabric.contrib.files import exists


env.hosts = ['winnuayi@192.168.1.2']
env.password = 'liverpool'
#env.hosts = ['dev@62.113.218.221']
#env.port = 13203
env.colorize_errors = True

PROJECTS_DEV_DIR = '~'
BACKEND_DIR = os.path.join(PROJECTS_DEV_DIR, 'www')
CIHEUL_DIR = os.path.join(BACKEND_DIR, 'ciheul')
VENV_DIR = os.path.join(PROJECTS_DEV_DIR, 'virtualenv')
VENV_CIHEUL_DIR = os.path.join(VENV_DIR, 'ciheul')

GIT_CIHEUL = 'https://github.com/ciheul/ciheul'


def setup():
    """Install all dependencies."""
    sudo("apt-get -y install nginx")

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


def clean():
    """Remove anything related to BigCrawler."""
    with cd(BACKEND_DIR):
        run("rm -rf ciheul")


def update_ciheul():
    """Update to the latest version."""
    with cd(CIHEUL_DIR):
        run('git pull')
