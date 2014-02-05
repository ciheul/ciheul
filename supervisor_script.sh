#!/bin/bash

set -e
LOGFILE=/var/log/gunicorn/ciheul.log
LOGDIR=$(dirname $LOGFILE)
NUM_WORKERS=2

# user/group to run as
USER=dev
GROUP=dev

cd ~/www/ciheul

source ~/virtualenv/ciheul/bin/activate

test -d $LOGDIR || mkdir -p $LOGDIR
exec gunicorn ciheul.wsgi:application -w $NUM_WORKERS 
  --user=$USER --group=$GROUP --log-level=debug 
  --log-file=$LOGFILE 2>>$LOGFILE
