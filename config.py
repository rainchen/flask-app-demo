from os import getenv


class BaseConfig(object):
  DEBUG = False
  SECRET_KEY = getenv("SECRET_KEY")
  SQLALCHEMY_DATABASE_URI = getenv("DATABASE_URL")


class ProductionConfig(BaseConfig):
  pass


class DevelopmentConfig(BaseConfig):
  DEBUG = True


class StagingConfig(BaseConfig):
  DEBUG = True


class TestingConfig(BaseConfig):
  TESTING = True
  SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@localhost/flask-app-demo-test?charset=utf8mb4"


config = {
    "development": DevelopmentConfig,
    "staging": StagingConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}
