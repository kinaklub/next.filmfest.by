#!/bin/bash
#
# Helper script to create web site previews on Netlify.

# It bootstraps Django to create static copy of website
# content and grabs it with wget into in `public/` dir.
#
# Produces `wget.log.txt` that can be downloaded for
# troubleshooting. Uses custom settings in 
# ../filmfest/settings/netlify.py
#
# Script should complete in 15 minutes.
#

set -x  # print lines being executed
set -e  # exit on first error

ROOTDIR=$(dirname $(dirname $0))
cd $ROOTDIR

echo --- [bootstrap] installing dependencies
pip install -r requirements/base.txt

echo --- [bootstrap] running migrations
# switch back from dev config to base
export DJANGO_SETTINGS_MODULE=filmfest.settings.netlify
export PYTHONUNBUFFERED=1
python manage.py migrate

echo --- [bootstrap] starting server in background
python manage.py runserver 127.0.0.1:8000 --insecure &
sleep 5

echo --- [bootstrap] grabbing site copy
mkdir public
cd public
wget -m http://127.0.0.1:8000 --no-host-directories 2>&1 | tee wget.log.txt
pwd
ls -la
ps aux

echo --- [bootstrap] stopping server
pkill -f manage.py

# returns 0, but we can also check wget exit code or
# log for 404 errors to fail build if there are any

#exit 0
