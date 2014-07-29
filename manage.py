#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
     try:
         with open('cloud/settings/local.py'):
             os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                                  "cloud.settings.local")
     except IOError:
         os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                              "cloud.settings.dev")

     from django.core.management import execute_from_command_line

     execute_from_command_line(sys.argv)
