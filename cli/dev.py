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

# pip package license compliance audit
# $ flask dev license_compliance_audit

import json
import os
import subprocess
import sys
from os import getenv

import click
from flask.cli import AppGroup
from prettytable import PrettyTable

dev_command = AppGroup(
    "dev",
    help="Audit code quality with code linter, formatter and security audit",
)
APP_DIR = os.path.abspath(os.path.dirname(__file__) + "/..")


@dev_command.command("lint")
@click.option(
    "--html-report",
    default=None,
    help=
    "Genereate html report, e.g. --html-report=tmp/dev/report/pylint-report.html",
)
@click.option(
    "--lowest-score",
    default=None,
    help=
    "Return exists status 1 if pylint_score(max is 10.0) is lower then --lowest-score, e.g. --lowest-score=8.0",
)
def lint(html_report, lowest_score):
  """Check coding style."""
  click.echo(click.style("Run linter", fg="cyan"))

  # prepare report dir
  report_dir = os.path.join(APP_DIR, "tmp/dev/report")
  os.makedirs(report_dir, exist_ok=True)

  os.system("pylint --version")
  click.echo("Linter Report:")
  # rcfile download from https://google.github.io/styleguide/pylintrc
  pylint_cli = "pylint --rcfile=devtools/google-pyguide.pylintrc"
  os.system(pylint_cli + " **/*.py --output-format=colorized")

  # genreate pylint-report.json
  if (html_report != None) or (lowest_score != None):
    # TODO: run pylint once only
    os.system(
        pylint_cli +
        " --load-plugins=pylint_report.pylint_report --output-format=pylint_report.pylint_report.CustomJsonReporter **/*.py > tmp/dev/report/pylint-report.json"
    )

  # generate a html report with https://github.com/drdv/pylint-report
  if html_report != None:
    # # genreate pylint-report.html
    os.system(
        "pylint_report.py tmp/dev/report/pylint-report.json --html-file %s" %
        html_report)
    click.echo("Generate a html report to %s" % html_report)

  # set $? to be none-zero if pylint_score is lower then lowest_score
  if lowest_score != None:
    allowed_lowest_score = float(lowest_score)
    import subprocess

    pylint_score = subprocess.getoutput(
        "pylint_report.py -s tmp/dev/report/pylint-report.json").split(": ")[1]
    if float(pylint_score) < allowed_lowest_score:
      click.echo(
          "[Error]The pylint_score %s is lower then lowest_score %s" %
          (pylint_score, allowed_lowest_score),
          err=True,
      )
      sys.exit(1)


# [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
@dev_command.command(
    "format",
    help=
    "Reformats codes to follow the Google Python Style Guide, returns zero exits status when no changes were necessary, non-zero otherwise.",
)
@click.option(
    "--in-place",
    default=False,
    is_flag=True,
    help="Make changes to files in place.",
)
def format(in_place):
  """Format codes with [Google Python Style Guide]."""
  click.echo(click.style("Run formatter", fg="cyan"))

  yapf_opt = "--diff"
  isort_opt = "--diff"
  if in_place:
    yapf_opt = "--in-place"
    isort_opt = ""
    click.echo(
        click.style("[NOTICE]Make changes to files in place!", fg="yellow"))

  sort_returncode, sort_stdout = _sort_imports(isort_opt)
  click.echo(click.style("sort import check result:", fg="magenta"))
  click.echo(sort_stdout)
  if b"---" in sort_stdout:  # mark find changes
    sort_returncode = 1

  format_returncode, format_stdout = _format_codes(yapf_opt)
  click.echo(click.style("format check result:", fg="magenta"))
  if not format_stdout:
    format_stdout = "No problem was found"
  click.echo(format_stdout)

  returncode = sort_returncode | format_returncode
  if not in_place:
    if returncode == 0:
      click.echo(click.style("No changes needed.", fg="green"))
    else:
      click.echo(click.style("Some changes needed.", fg="red"))
  # returns zero when no changes were necessary
  sys.exit(returncode)


def _format_codes(yapf_opt):
  """format codes using yapf CLI"""
  # consisting with pylint that using google style for indent_width: 2
  yapf_cmd = (
      'yapf --style="{based_on_style: google, indent_width: 2}" %s --recursive .'
      % yapf_opt)
  proc = subprocess.run(yapf_cmd, shell=True, capture_output=True)  # nosec
  return proc.returncode, proc.stdout


def _sort_imports(isort_opt=""):
  """sort imports using isort CLI"""
  isort_cmd = "isort  %s ." % isort_opt
  proc = subprocess.run(isort_cmd, shell=True, capture_output=True)  # nosec
  return proc.returncode, proc.stdout


@dev_command.command("security_audit")
@click.option(
    "--html-report",
    default=None,
    help=
    "Genereate html report, e.g. --html-report=tmp/dev/report/bandit-report.html",
)
@click.option("--debug",
              default=None,
              is_flag=True,
              help="Show more info for debugging")
def security_audit(html_report, debug):
  """Code security audit."""
  click.echo(click.style("Run security audit", fg="cyan"))

  bandit_opt = "--recursive . --ini devtools/bandit.ini"
  capture_output = (
      False  # don't capture output to show colorize output in Shell
  )
  if html_report != None:
    bandit_opt += " --format html"
    capture_output = True

  bandit_cmd = "bandit %s" % bandit_opt

  if debug != None:
    click.echo("execute cmd: $ %s" % bandit_cmd)
  proc = subprocess.run(
      bandit_cmd,
      shell=True,  # nosec
      capture_output=capture_output,
      universal_newlines=True,
  )

  if html_report != None:
    report = open(html_report, "w")
    report.write(proc.stdout)
    report.close()

    click.echo("Generate a html report to %s" % html_report)

  # show audit result
  if proc.returncode == 0:
    click.echo(click.style("No security issues found.", fg="green"))
  else:
    click.echo(click.style("Found some security issues.", fg="red"))

  sys.exit(proc.returncode)


@dev_command.command(
    "license_compliance_audit",
    help="Check license compliance of 3rd party dependencies.",
)
def license_compliance_audit():
  """open source license compliance"""
  # popular licenses table: https://choosealicense.com/appendix/
  # popular licenses list: https://choosealicense.com/licenses/
  # licenses approved by the OSI: https://opensource.org/licenses/alphabetical
  click.echo(
      click.style(
          "Check open source license compliance according to config in .env",
          fg="cyan",
      ))
  cmd = "pip-licenses --order=license --format=json"
  allowed_licenses = getenv(
      "FLASK_DEV_LICENSE_COMPLIANCE_AUDIT_ALLOWED_LICENSES", "").split(",")
  ignored_packages = getenv(
      "FLASK_DEV_LICENSE_COMPLIANCE_AUDIT_IGNORED_PACKAGES", "").split(",")
  proc = subprocess.run(cmd, shell=True, capture_output=True)  # nosec
  if proc.returncode == 0:
    audit_result = json.loads(proc.stdout)
    # filter out licenses which x['License'] neither in allowed_licenses nor x['Name'] not in ignored_packages, x['License'] could be a string combined with "; "
    filtered_audit_result = [
        x for x in audit_result
        if (not all(i in allowed_licenses for i in x["License"].split("; ")) and
            x["Name"] not in ignored_packages)
    ]
  if len(filtered_audit_result) == 0:
    click.echo(click.style("Audit Passed!", fg="green"))
  else:
    click.echo(click.style("Audit Failed!", fg="red"))
    # show audit result in table format using PrettyTable
    table = PrettyTable(["Name", "Version", "License"])
    for x in filtered_audit_result:
      table.add_row([x["Name"], x["Version"], x["License"]])
    click.echo(table)
    click.echo(
        click.style(
            "Run `pipenv graph` to displays currently-installed dependency graph in a tree view.",
            fg="cyan",
        ))
    click.echo(
        click.style(
            "Use alternative packages or set these packages as ignored_packages/whitelist in config .env.",
            fg="cyan",
        ))
    sys.exit(1)
