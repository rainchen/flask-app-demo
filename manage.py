from os import getenv

from flask_migrate import Migrate
from flask_script import Manager

from api.datab import db
from config import config
from main import create_app

from sqlalchemy_utils import create_database 

config_name = getenv("FLASK_ENV", "production")
app = create_app(config.get(config_name))
migrate = Migrate(app, db)
manager = Manager(app)

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
