import json

from flask import Response

from api.controllers.base_controller import BaseController
from api.models import User

class UserController(BaseController):
    def get(self, *args, **kwargs):
        user_id = self.request.view_args.get("user_id")
        if user_id == None:
            data = self.list()
        else:
            data = self.show(user_id)

        return Response(
            json.dumps({"msg": "ok", "data": data}), content_type="application/json"
        )

    def list(self):
        users = User.query.all()
        return list(map(self.__format_user, users))

    def show(self, user_id):
        user = User.query.filter_by(id=user_id).one()
        return self.__format_user(user)


    def post(self, *args, **kwargs):
        pass

    @staticmethod
    def __format_user(user):
        return {
         "id": user.id,
         "username": user.username,
         "first_name": user.first_name,
         "last_name": user.last_name,
        }
