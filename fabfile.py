import os
from contextlib import contextmanager
from fabric.api import *
from fabric.contrib.files import exists, sed
from urlparse import urlsplit


# main configuration
env.hosts = [
#        'winnuayi@192.168.1.2:22',
#        'winnuayi@192.168.1.3:22', 
         'dev@192.168.1.3',
#        'dev@62.113.218.221:13203',
]

# root directory
env.directories = {
        "production": '~',
        "development": '~',        
        "development_proj": '~/Projects/dev'        
}

env.roledefs = {
    "development": ["192.168.1.3"],
    "development_proj": ["192.168.1.2"],
    "production": ["192.168.1.3", "62.113.218.221"],
}

# invert roledefs
env.invert_roledefs = {}
for i in env.roledefs:
    for j in env.roledefs[i]:
        env.invert_roledefs[j] = i

# misc. configuration
env.colorize_errors = True

# github
GIT_CIHEUL = 'https://github.com/ciheul/ciheul'


def init_directory():
    """Production and Development server have different project root 
       directory."""
    o = urlsplit('ssh://' + env.host_string)
    env.PROJECTS_DEV_DIR = env.directories[env.invert_roledefs[o.hostname]]
    env.WWW_DIR = os.path.join(env.PROJECTS_DEV_DIR, 'www')
    env.CIHEUL_DIR = os.path.join(env.WWW_DIR, 'ciheul')
    env.VENV_DIR = os.path.join(env.PROJECTS_DEV_DIR, 'virtualenv')
    env.VENV_CIHEUL_DIR = os.path.join(env.VENV_DIR, 'ciheul')


def setup():
    """Install all dependencies."""
    with settings(warn_only=True):
        sudo("apt-get -y install nginx")
        # check following link to login:
        # - https://help.ubuntu.com/community/PostgreSQL
        sudo("apt-get -y install postgresql")
        sudo("apt-get -y install redis-server")
        sudo("apt-get -y install rabbitmq-server")

        sudo("apt-get -y install libevent-dev")
        sudo("apt-get -y install libpq-dev")
        sudo("apt-get -y install gcc g++")
        sudo("apt-get -y install python-dev")
        sudo("apt-get -y install openjdk-6-jdk")
        # GIS
        sudo("apt-get -y install gdal-bin")
        sudo("apt-get -y install supervisor")
        sudo("apt-get -y install python-pip")

        
        sudo("pip install virtualenv")


@task
#@parallel
def deploy():
    """Deploy Ciheul.com web."""
    setup()
    init_directory()

    # create virtualenv for ciheul if necessary
    if not exists(env.VENV_CIHEUL_DIR):
        run("mkdir -p " + env.VENV_DIR)
        with cd(env.VENV_DIR):
            run("virtualenv ciheul")

    # for the first time, git clone. otherwise, ignore
    if not exists(env.CIHEUL_DIR):
        run("mkdir -p " + env.WWW_DIR)
        with cd(env.WWW_DIR):
            run('git clone ' + GIT_CIHEUL)

    # install python packages using pip
    with prefix("source " + os.path.join(env.VENV_CIHEUL_DIR, 'bin/activate')):
        with cd(env.CIHEUL_DIR):
            run("pip install -r requirements.txt")

    # send config file.
    put('ciheul/config.py', os.path.join(env.CIHEUL_DIR, 'ciheul/config.py'))

    # create directory for supervisor output if necessary
    sudo('mkdir -p /var/log/supervisor')

    # copy ciheul's supervisor configuration to supervisor directory
    put('supervisor_ciheul.conf', '/etc/supervisor/conf.d/ciheul.conf', 
        use_sudo=True)

    # replace command path depends on its different directory.
    # check 'env.directories'. pwd command to recognize ciheul directory.
    with cd(env.CIHEUL_DIR):
        x = run("echo `pwd`")
    sed("/etc/supervisor/conf.d/ciheul.conf", "replace_ciheul_dir", x, 
        use_sudo=True)
        
    # update supervisor
    sudo('supervisorctl reread && supervisorctl update')
    #sudo('supervisorctl start ciheul')


@task
#@parallel
def clean():
    """Remove anything related to Ciheul."""
    init_directory()

    # remove ciheul web directory
    with cd(env.WWW_DIR):
        run("rm -rf ciheul")

    # remove ciheul virtualenv
    #with cd(env.VENV_DIR):
    #    run("rm -rf ciheul")

    # stop supervisor for ciheul
    sudo('supervisorctl stop ciheul && supervisorctl remove ciheul')
    with settings(warn_only=True):
        run("pkill gunicorn")



@task
def update():
    """Update to the latest version."""
    init_directory()
    with cd(env.CIHEUL_DIR):
        run('git stash')
        run('git pull')

    # install python packages using pip
    with prefix("source " + os.path.join(env.VENV_CIHEUL_DIR, 'bin/activate')):
        with cd(env.CIHEUL_DIR):
            put('requirements.txt', \
                    os.path.join(env.CIHEUL_DIR, 'requirements.txt'))
            run("pip install -r requirements.txt")
            
            put('start_gunicorn_socketio.sh', \
                    os.path.join(env.CIHEUL_DIR, 'start_gunicorn_socketio.sh'))


@task
#@roles('production')
def cmd(command):
    with settings(warn_only=True):
        run(command)


@task
@parallel
def echo():
    init_directory()
    run("echo " + env.PROJECTS_DEV_DIR)
    run("echo " + env.WWW_DIR)
    run("echo " + env.CIHEUL_DIR)
    run("echo " + env.VENV_DIR)
    run("echo " + env.VENV_CIHEUL_DIR)


@task
@with_settings(warn_only=True)
def super():
    init_directory()
    with cd(env.CIHEUL_DIR):
        #sudo("x=$(echo `pwd`/start_django.sh | sed \"s/\//\\\//g\"); sed -i \"s/{{command}}/$x/g\" /etc/supervisor/conf.d/ciheul.conf")
        #x = run("echo `pwd`/start_django.sh | sed \"s/\//\\\//g\"")
        x = run("echo `pwd`/start_django.sh")
    sed("/etc/supervisor/conf.d/ciheul.conf", "replace_cmd_path", x, use_sudo=True)
