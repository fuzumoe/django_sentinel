#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pydj_auth.settings')
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
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        import subprocess
        # Map custom test shortcuts to pytest args
        if len(sys.argv) > 2 and sys.argv[2] == "unit":
            pytest_args = ["pytest", "pydj_auth/tests/unit"] + sys.argv[3:]
        elif len(sys.argv) > 2 and sys.argv[2] == "e2e":
            pytest_args = ["pytest", "pydj_auth/tests/e2e"] + sys.argv[3:]
        elif len(sys.argv) > 2:
            pytest_args = ["pytest"] + sys.argv[2:]
        else:
            pytest_args = ["pytest", "pydj_auth/tests"] + sys.argv[3:]
        raise SystemExit(subprocess.call(pytest_args))
    main()