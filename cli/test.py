# set in manage.py
# app.cli.add_command(test_command, "test")

# in terminal:
# $ flask test

import click
from flask.cli import with_appcontext


@click.command()
@with_appcontext
def test_command():
  """Run test, same as running $ python -m unittest."""
  # import os
  # os.system("python -m unittest")

  # same as executing unittest/__main__.py
  __unittest = True
  import sys
  sys.argv = ['python' + " -m unittest"]
  import unittest
  unittest.main(module=None)
