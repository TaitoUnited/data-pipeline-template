#!/usr/bin/env python3
"""Django's command-line utility for administrative tasks."""
import os
import sys


def read_secret(name):
    with open("/run/secrets/" + name, "r") as f:
        value = f.readline()
    return value


def set_environ_secret(name):
    try:
        os.environ.setdefault(name, read_secret(name))
    except os.OSError:
        os.environ.setdefault(os.environ.get(name))


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
    set_environ_secret("DATABASE_PASSWORD")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
