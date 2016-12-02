#!/bin/bash
#
# Bootstrap Django and create static site copy
# for Netlily development previews
#

ROOTDIR=$(dirname $(dirname $0))
cd $ROOTDIR

echo [bootstrap] creating virtualenv in .v
virtualenv .v
.v/bin/pip install -r requirements/base.txt
