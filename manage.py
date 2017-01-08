#!/usr/bin/env python
import os
import sys


def main():
    settings_module = os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                                            "filmfest.settings.dev")
    cmd = (sys.argv[1:2] + [None])[0]
    args = sys.argv[2:]

    if cmd == 'test':
        import tox
        sys.exit(tox.cmdline(args))
    elif cmd == 'bash':
        from subprocess import call
        sys.exit(call('/usr/bin/bash', *args))
    elif cmd == 'launch':
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
    else:
        from django.core.management import execute_from_command_line
        execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
