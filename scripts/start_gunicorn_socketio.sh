#!/bin/bash

# get project dev directory
cd ../../..
PROJECTS_DEV_DIR=$(pwd)
echo "PROJECTS_DEV_DIR="$PROJECTS_DEV_DIR

# activate virtualenv to isolate environment
source $PROJECTS_DEV_DIR/virtualenv/ciheul/bin/activate

# start running django with gunicorn
cd $PROJECTS_DEV_DIR/www/ciheul
exec gunicorn --worker-class socketio.sgunicorn.GeventSocketIOWorker ciheul.wsgi:application
