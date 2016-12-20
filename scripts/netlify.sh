#!/bin/bash
#
# Bootstrap Django and create static site copy
# for Netlily development previews
#
# Netlify timeout for builds is 15 minutes
#

ROOTDIR=$(dirname $(dirname $0))
cd $ROOTDIR

echo --- [bootstrap] creating virtualenv in .v
virtualenv .v
.v/bin/pip install -r requirements/base.txt

echo --- [bootstrap] running migrations
# switch back from dev config to base
export DJANGO_SETTINGS_MODULE=filmfest.settings.netlify
export PYTHONUNBUFFERED=1
.v/bin/python manage.py migrate

echo --- [bootstrap] starting server in background
.v/bin/python manage.py runserver 127.0.0.1:8000 --insecure &
sleep 5

echo --- [bootstrap] grabbing site copy
mkdir public
cd public
wget -m http://127.0.0.1:8000 --no-host-directories 2>&1 | tee wget.log
pwd
ls -la

exit 0