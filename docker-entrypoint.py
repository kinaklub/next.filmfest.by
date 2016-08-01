#!/app/bin/python
import os
import sys


with open('/app/IMAGE_VERSION') as f:
    IMAGE_VERSION = f.read().strip()

with open('/app/src/IMAGE_VERSION') as f:
    CODE_IMAGE_VERSION = f.read().strip()

if CODE_IMAGE_VERSION != IMAGE_VERSION:
    sys.stderr.write(
        (
            'Docker image version is {IMAGE_VERSION} '
            'but it\'s expected to be {CODE_VERSION}\n'
            '\n'
            'Try to rebuild the image with:\n'
            '\n'
            '    docker-compose build web\n'
        ).format(IMAGE_VERSION=IMAGE_VERSION, CODE_VERSION=CODE_IMAGE_VERSION)
    )
    sys.exit(17)

os.execl(sys.executable, sys.executable, 'manage.py', *sys.argv[1:])
