# set in manage.py
# from cli.dev import dev_command
# app.cli.add_command(dev_command, "dev")

# in Terminal:
# $ flask dev

# run linter and generate html report
# $ flask dev lint --html-report=tmp/dev/report/pylint-report.html

# config lowest lint score, useful for CI
# $ flask dev lint --lowest-score=8.0
# $? will be none-zero if pylint_score is lower then lowest_score

from flask.cli import AppGroup
import click
import os
import sys

dev_command = AppGroup('dev', help='Audit code quality with code linter, formatter and security audit')
APP_DIR = os.path.abspath(os.path.dirname(__file__) + "/..")

@dev_command.command('lint')
@click.option('--html-report', default=None, help='Genereate html report, e.g. --html-report=tmp/dev/report/pylint-report.html')
@click.option('--lowest-score', default=None, help='Return exists status 1 if pylint_score(max is 10.0) is lower then --lowest-score, e.g. --lowest-score=8.0')
def lint(html_report, lowest_score):
    """Check coding style."""
    click.echo(click.style("Run linter", fg='green'))

    # prepare report dir
    report_dir = os.path.join(APP_DIR, "tmp/dev/report")
    os.makedirs(report_dir, exist_ok=True)

    os.system('pylint --version')
    click.echo("Linter Report:")
    os.system('pylint **/*.py --output-format=colorized')

    # genreate pylint-report.json
    if (html_report != None) or (lowest_score != None):
        # TODO: run pylint once only
        os.system('pylint --load-plugins=pylint_report.pylint_report --output-format=pylint_report.pylint_report.CustomJsonReporter **/*.py > tmp/dev/report/pylint-report.json')

    # generate a html report with https://github.com/drdv/pylint-report
    if html_report != None:
        # # genreate pylint-report.html
        os.system('pylint_report.py tmp/dev/report/pylint-report.json --html-file %s' % html_report)
        click.echo('Generate a html report to %s' % html_report)

    # set $? to be none-zero if pylint_score is lower then lowest_score
    if lowest_score != None:
        allowed_lowest_score = float(lowest_score)
        import subprocess
        pylint_score = subprocess.getoutput("pylint_report.py -s tmp/dev/report/pylint-report.json").split(": ")[1]
        if float(pylint_score) < allowed_lowest_score:
            click.echo("[Error]The pylint_score %s is lower then lowest_score %s" % (pylint_score, allowed_lowest_score), err=True)
            sys.exit(1)

# [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
@dev_command.command('format')
def format():
    """Format codes with [Google Python Style Guide]."""
    print("run formatter")

@dev_command.command('security_audit')
def security_audit():
    """Code security audit."""
    print("run security audit")
