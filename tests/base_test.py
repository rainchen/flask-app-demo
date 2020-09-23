from flask_testing import TestCase
from sqlalchemy_utils import create_database, database_exists

from config import config
from main import create_app, db

app = create_app(config.get("testing"))


class BaseTestCase(TestCase):

    def create_app(self):
        app.config.from_object(config.get("testing"))
        return app

    def setUp(self):
        self.__create_db()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def __create_db(self):
        db_uri = config.get("testing").SQLALCHEMY_DATABASE_URI
        db_name = db.engine.url.database
        if database_exists(db_uri) == False:
            print("create db: ", db_name)
            create_database(db_uri)
