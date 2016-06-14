#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mmkit2.settings")
    os.environ.setdefault("BASE_DIR", os.path.dirname(os.path.abspath(__file__)))
    os.environ.setdefault("APP_ENV", 'prod')

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
