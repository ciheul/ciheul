#!/bin/bash

redis-server &

cd ../..
PROJECTS_DEV_DIR=$(pwd)
echo $PROJECTS_DEV_DIR
source $PROJECTS_DEV_DIR/virtualenv/ciheul/bin/activate

cd $PROJECTS_DEV_DIR/www/ciheul
exec celery -A ciheul.jendela24 worker & #--loglevel=debug

exec gunicorn --worker-class socketio.sgunicorn.GeventSocketIOWorker ciheul.wsgi:application &
