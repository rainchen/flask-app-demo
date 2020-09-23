# set in manage.py
# from cli.dev import dev_command
# app.cli.add_command(dev_command, "dev")

# in Terminal:
# $ flask dev

# run linter and generate html report
# $ flask dev lint --html-report=tmp/dev/report/pylint-report.html

# config lowest lint score, useful for CI
# $ flask dev lint --lowest-score=8.0
# $? will be non-zero if pylint_score is lower then lowest_score

# format codes
# $ flask dev format
# $? will be non-zero if some files need to be changed

# format codes and make changes to files in place
# $ flask dev format --in-place

import os
import subprocess
import sys

import click
from flask.cli import AppGroup

dev_command = AppGroup(
    'dev',
    help='Audit code quality with code linter, formatter and security audit')
APP_DIR = os.path.abspath(os.path.dirname(__file__) + "/..")


@dev_command.command('lint')
@click.option(
    '--html-report',
    default=None,
    help=
    'Genereate html report, e.g. --html-report=tmp/dev/report/pylint-report.html'
)
@click.option(
    '--lowest-score',
    default=None,
    help=
    'Return exists status 1 if pylint_score(max is 10.0) is lower then --lowest-score, e.g. --lowest-score=8.0'
)
def lint(html_report, lowest_score):
    """Check coding style."""
    click.echo(click.style("Run linter", fg='cyan'))

    # prepare report dir
    report_dir = os.path.join(APP_DIR, "tmp/dev/report")
    os.makedirs(report_dir, exist_ok=True)

    os.system('pylint --version')
    click.echo("Linter Report:")
    os.system('pylint **/*.py --output-format=colorized')

    # genreate pylint-report.json
    if (html_report != None) or (lowest_score != None):
        # TODO: run pylint once only
        os.system(
            'pylint --load-plugins=pylint_report.pylint_report --output-format=pylint_report.pylint_report.CustomJsonReporter **/*.py > tmp/dev/report/pylint-report.json'
        )

    # generate a html report with https://github.com/drdv/pylint-report
    if html_report != None:
        # # genreate pylint-report.html
        os.system(
            'pylint_report.py tmp/dev/report/pylint-report.json --html-file %s'
            % html_report)
        click.echo('Generate a html report to %s' % html_report)

    # set $? to be none-zero if pylint_score is lower then lowest_score
    if lowest_score != None:
        allowed_lowest_score = float(lowest_score)
        import subprocess
        pylint_score = subprocess.getoutput(
            "pylint_report.py -s tmp/dev/report/pylint-report.json").split(
                ": ")[1]
        if float(pylint_score) < allowed_lowest_score:
            click.echo(
                "[Error]The pylint_score %s is lower then lowest_score %s" %
                (pylint_score, allowed_lowest_score),
                err=True)
            sys.exit(1)


# [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
@dev_command.command(
    'format',
    help=
    'Reformats codes to follow the Google Python Style Guide, returns zero exits status when no changes were necessary, non-zero otherwise.'
)
@click.option('--in-place',
              default=False,
              is_flag=True,
              help='Make changes to files in place.')
def format(in_place):
    """Format codes with [Google Python Style Guide]."""
    click.echo(click.style("Run formatter", fg='cyan'))

    yapf_opt = '--diff'
    isort_opt = '--diff'
    if in_place:
        yapf_opt = '--in-place'
        isort_opt = ''
        click.echo(
            click.style("[NOTICE]Make changes to files in place!", fg='yellow'))

    sort_returncode, sort_stdout = _sort_imports(isort_opt)
    click.echo(click.style('sort import check result:', fg='magenta'))
    click.echo(sort_stdout)
    if b'---' in sort_stdout:  # mark find changes
        sort_returncode = 1

    format_returncode, format_stdout = _format_codes(yapf_opt)
    click.echo(click.style('format check result:', fg='magenta'))
    if not format_stdout:
        format_stdout = 'No problem was found'
    click.echo(format_stdout)

    returncode = (sort_returncode | format_returncode)
    if not in_place:
        if returncode == 0:
            click.echo(click.style('No changes needed.', fg='green'))
        else:
            click.echo(click.style('Some changes needed.', fg='red'))
    # returns zero when no changes were necessary
    sys.exit(returncode)


def _format_codes(yapf_opt):
    """format codes using yapf CLI"""
    yapf_cmd = 'yapf --style="{based_on_style: google}" %s --recursive **/*.py' % yapf_opt
    proc = subprocess.run(yapf_cmd, shell=True, capture_output=True)
    return proc.returncode, proc.stdout


def _sort_imports(isort_opt=''):
    """sort imports using isort CLI"""
    isort_cmd = 'isort  %s .' % isort_opt
    proc = subprocess.run(isort_cmd, shell=True, capture_output=True)
    return proc.returncode, proc.stdout


@dev_command.command('security_audit')
def security_audit():
    """Code security audit."""
    print("run security audit")
