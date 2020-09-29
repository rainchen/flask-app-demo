from os import getenv

from flask_migrate import Migrate
from flask_script import Manager
from sqlalchemy_utils import create_database

from api.datab import db
from cli.dev import dev_command
from cli.test import test_command
from config import config
from main import create_app

config_name = getenv("FLASK_ENV", "production")
app = create_app(config.get(config_name))
migrate = Migrate(app, db)
manager = Manager(app)
# add custom cli commands
app.cli.add_command(test_command, "test")
app.cli.add_command(dev_command, "dev")


# add cli command: flask create-db
@app.cli.command()
def create_db():
  """Create the configured database."""
  db_uri = config.get(config_name).SQLALCHEMY_DATABASE_URI
  db_name = db.engine.url.database
  print("create db: ", db_name)
  create_database(db_uri)


if "__main__ " == __name__:
  manager.run()
