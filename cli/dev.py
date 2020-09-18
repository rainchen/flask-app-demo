# set in manage.py
# from cli.dev import dev_command
# app.cli.add_command(dev_command, "dev")

# in Terminal:
# $ flask dev

from flask.cli import AppGroup

dev_command = AppGroup('dev', help="Audit code quality with code linter, formatter and security audit")

@dev_command.command('lint')
def lint():
    """Check coding style."""
    print("run linter")

# [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
@dev_command.command('format')
def format():
    """Format codes with [Google Python Style Guide]."""
    print("run formatter")

@dev_command.command('security_audit')
def security_audit():
    """Code security audit."""
    print("run security audit")
