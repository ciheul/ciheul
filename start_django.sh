#!/bin/bash

#set -e
#LOGFILE=/var/log/gunicorn/ciheul.log
#LOGDIR=$(dirname $LOGFILE)
NUM_WORKERS=2

# user/group to run as
#USER=winnuayi
#GROUP=winnuayi

# get project dev directory
cd ../..
PROJECTS_DEV_DIR=$(pwd)
echo $PROJECTS_DEV_DIR

# create folder for logging if necessary
#test -d $LOGDIR || sudo mkdir -p $LOGDIR

# activate virtualenv to isolate environment
source $PROJECTS_DEV_DIR/virtualenv/ciheul/bin/activate

# start running django with gunicorn
cd $PROJECTS_DEV_DIR/www/ciheul
exec gunicorn ciheul.wsgi:application -w $NUM_WORKERS
