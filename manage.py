#!/usr/bin/env python3
"""Django's command-line utility for administrative tasks.

This file is a thin wrapper placed at the project root so CI tools
and Makefile targets that expect `manage.py` here can find it.
It delegates to the Django project in `task_manager`.
"""
import os
import sys


def main() -> None:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "task_manager.settings")
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()

