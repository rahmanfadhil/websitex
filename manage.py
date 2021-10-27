#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def initialize_vscode_debugger():
    """
    Initialize VSCode debugger on port 9999.

    https://ytec.nl/blog/debugging-django-vscode-without-using-noreload/
    https://testdriven.io/blog/django-debugging-vs-code/
    """
    from django.conf import settings

    if settings.DEBUG and os.environ.get("RUN_MAIN"):
        import debugpy

        debugpy.listen(("0.0.0.0", 9999))
        print("Debugger attached, starting server...")


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myapp.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    initialize_vscode_debugger()
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
