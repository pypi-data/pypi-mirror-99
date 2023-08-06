import argparse
import os
import sys

try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'example.settings')
    import django
    from django.core.management import call_command
except ImportError as exc:
    raise ImportError(
        "Couldn't import Django. Are you sure it's installed and "
        "available on your PYTHONPATH environment variable? Did you "
        "forget to activate a virtual environment?"
    ) from exc

from .commands import call_migrate, call_collect_static
from .health_check import health_check


def get_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument('--migrate', action='store_true')
    parser.add_argument('--collectstatic', action='store_true')
    parser.add_argument('--health-check', action='store_true')
    parser.add_argument('--silent', action='store_true')
    return parser


def setup_django() -> None:
    django.setup()


def django_main():
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    arg_parser = get_arg_parser()
    args = arg_parser.parse_known_args()

    if args[0].health_check:
        exit(health_check(args[0].silent))

    setup_django()

    if args[0].collectstatic:
        call_collect_static()

    if args[0].migrate:
        call_migrate()

    sys.argv = [sys.argv[0], *args[1]]
    django_main()
