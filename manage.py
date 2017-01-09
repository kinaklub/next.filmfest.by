#!/usr/bin/env python
import os
import sys


def test(args, settings_module):
    """Launch tests via tox"""
    import tox
    sys.exit(tox.cmdline(args))


def bash(args, settings_module):
    """Launch bash session"""
    from subprocess import call
    sys.exit(call('/usr/bin/bash', *args))


def launch(args, settings_module):
    """Launch the application"""
    from django.core.management import execute_from_command_line
    execute_from_command_line(['manage.py', 'migrate'])

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
    ]
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
