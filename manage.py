#!/usr/bin/env python
import os
import sys
import time


def test(args, settings_module):
    """Launch tests via tox"""
    import tox
    sys.exit(tox.cmdline(args))


def bash(args, settings_module):
    """Launch bash session"""
    from subprocess import call
    sys.exit(call('/usr/bin/bash', *args))


def _wait_for_db(sleep_interval=2, max_wait=600):
    """Wait for DB container to start"""
    from django.db import connections
    from django.db.utils import OperationalError

    t0 = time.time()
    while True:
        try:
            connections['default'].cursor()
        except OperationalError:
            if time.time() - t0 > max_wait:
                raise
            else:
                print "Waiting for DB initialization"
                time.sleep(sleep_interval)
        else:
            break


def _wait_for_elasticsearch(sleep_interval=2, max_wait=600):
    """Wait for elasticsearch container to start"""
    from elasticsearch import ConnectionError
    from wagtail.wagtailsearch.backends import get_search_backend

    es = get_search_backend('default').es
    t0 = time.time()
    while True:
        try:
            if es.ping():
                break
        except ConnectionError:
            if time.time() - t0 > max_wait:
                raise
        else:
            if time.time() - t0 > max_wait:
                raise Exception('Give up waiting for elasticsearch')

        print "Waiting for elasticsearch initialization"
        time.sleep(sleep_interval)


def launch(args, settings_module):
    """Launch the application"""
    from django.conf import settings
    from django.core.management import execute_from_command_line

    _wait_for_db()
    execute_from_command_line(['manage.py', 'migrate', '--noinput'])
    _wait_for_elasticsearch()
    execute_from_command_line(['manage.py', 'update_index'])

    http_socket = (args[:1] + [':8000'])[0]
    uwsgi_args = [
        'uwsgi',
        '--module', 'filmfest.wsgi',
        '--env', 'DJANGO_SETTINGS_MODULE={}'.format(settings_module),
        '--http-socket', http_socket,
        '--master',
        '--harakiri=120',
        '--max-requests=1000',
        '--vacuum',
        '--static-map', '%s=%s' % (settings.MEDIA_URL, settings.MEDIA_ROOT),
    ]
    if settings.DEBUG:
        uwsgi_args.extend([
            '--py-autoreload', '1',
        ])
    else:
        uwsgi_args.extend([
            '--static-map', '%s=%s' % (settings.STATIC_URL,
                                       settings.STATIC_ROOT)
        ])

    if sys.real_prefix:
        # we are in a virtual env - let's take it into account
        uwsgi_args.extend(['--home', sys.prefix])
        os.execv(os.path.join(sys.prefix, 'bin', 'uwsgi'), uwsgi_args)
    else:
        os.execvp('uwsgi', uwsgi_args)


def django(args, settings_module):
    """Call django manage.py handler"""
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)


def main():
    settings_module = os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                                            "filmfest.settings.dev")
    cmd = (sys.argv[1:2] + [None])[0]
    args = sys.argv[2:]

    handler = {
        'test': test,
        'bash': bash,
        'launch': launch,
    }.get(cmd, django)

    return handler(args, settings_module)


if __name__ == "__main__":
    main()
