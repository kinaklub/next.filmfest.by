#!/usr/bin/env python
import os
import sys


def main():
    if sys.argv[1:2] == ['test']:
        import tox
        sys.exit(tox.cmdline(sys.argv[2:]))
    elif sys.argv[1:2] == ['bash']:
        from subprocess import call
        sys.exit(call('/usr/bin/bash', *sys.argv[2:]))
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                              "filmfest.settings.dev")
        from django.core.management import execute_from_command_line
        execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
