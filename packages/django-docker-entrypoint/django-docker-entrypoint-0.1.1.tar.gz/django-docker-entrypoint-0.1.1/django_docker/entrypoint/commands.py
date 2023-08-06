from django.core.management import call_command


def call_collect_static(silent=False) -> None:
    cmd = ['collectstatic', '--no-input', '-i', '*.html', '-i', '*.map']
    if silent:
        cmd.append('-v0')
    call_command(*cmd)


def call_migrate(silent=False) -> None:
    cmd = ['migrate', '--no-input']
    if silent:
        cmd.append('-v0')
    call_command(*cmd)
