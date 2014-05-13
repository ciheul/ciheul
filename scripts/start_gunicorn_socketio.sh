#!/bin/bash

cd ../..
PROJECTS_DEV_DIR=$(pwd)
echo $PROJECTS_DEV_DIR
source $PROJECTS_DEV_DIR/virtualenv/ciheul/bin/activate

cd $PROJECTS_DEV_DIR/www/ciheul

exec gunicorn --worker-class socketio.sgunicorn.GeventSocketIOWorker ciheul.wsgi:application
