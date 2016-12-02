#!/bin/bash
#
# Bootstrap Django and create static site copy
# for Netlily development previews
#

BASEDIR=$(dirname $0)
cd $BASEDIR

echo [bootstrap] creating virtualenv in .v
virtualenv .v
.v/bin/pip install -r requirements/base.txt
