from flask import request
import sqlalchemy
import werkzeug


class BaseBluePrint(object):
    def __init__(self, app=None):
        self.app = app

    def register(self):
        self.app.register_error_handler(Exception, self.error_handler)

        from api.blueprints.users import users_blueprint

        self.app.register_blueprint(users_blueprint)

    def error_handler(self, err):
        msg = "Request resulted in {}".format(err)

        if isinstance(err, (sqlalchemy.orm.exc.NoResultFound, werkzeug.exceptions.NotFound)):
            return self.handle_404_exception(err)
        else:
            self.app.logger.warning(msg, exc_info=err)
            return {'msg': msg}, 500

    def handle_404_exception(self, err):
        msg = "Request resulted in {}".format(err)
        return {'msg': msg}, 404
