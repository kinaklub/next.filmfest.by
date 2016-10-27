#!/usr/bin/env python
"""
Checks data files for errors. Recursively scans current dir.
Checks implemented:

* [x] all images are present
* [x] images that are not used

requires: tablib
"""

import os
import sys

import tablib

errors = 0
imageindex = []
imagedirs = []


def error(msg):
    global errors
    print("    error - " + msg)
    errors += 1


file_checks = [
    {
        'file': 'partners.json',
        'image_field': 'image',
    },
    {
        'file': 'films.json',
        'image_field': 'frame',
    },
]


def checkimage(images):
    for image in images:
        # check that image does not exist
        imagepath = os.path.join(os.path.dirname(filename), image)
        if not os.path.exists(imagepath):
            error("missing '%s'" % os.path.normpath(imagepath))
        else:
            # check that image reused
            fullpath = os.path.normpath(imagepath)
            if fullpath in imageindex:
                print("    hmm - image reused '%s'" % imagepath)
            else:
                # store full path
                imageindex.append(fullpath)

def datacheck(filename):
    global imageindex
    global imagedirs

    print(filename)
    data = tablib.Dataset().load(open(filename).read())
    print("  entries: %s" % len(data))
    for file_check in file_checks:
        if filename.endswith(file_check['file']):
            checkimage(data[file_check['image_field']])


def extraimages():
    """Find images not referenced through any checks"""
    global imageindex

    imagedirs = set()
    for fullpath in imageindex:
        path = os.path.normpath(os.path.dirname(fullpath))
        if path not in imagedirs:
            imagedirs.add(path)
    for d in imagedirs:
        for root, dirs, files in os.walk(d):
            for name in files:
                filename = os.path.join(root, name)
                if filename not in imageindex:
                    error("extra '%s'" % filename)


for root, dirs, files in os.walk('.'):
    for name in files:
        filename = os.path.join(root, name)
        if filename.endswith('.json'):
            datacheck(filename)


extraimages()

if not errors:
    print('all ok')
else:
    sys.exit(errors)
