from api.models import User
from tests.base_test import BaseTestCase


class TestApiUsers(BaseTestCase):

  def test_list_users(self):
    response = self.client.get("/users")
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json, {'data': [], 'msg': 'ok'})

    # DRY these lines of codes with one line
    # from main import db
    # user = User(username='admin', first_name='Ming', last_name='Li')
    # db.session.add(user)
    # db.session.commit()

    User.create(username='admin', first_name='Ming', last_name='Li')

    response = self.client.get("/users")
    self.assertEqual(response.status_code, 200)
    self.assertEqual(
        response.json, {
            'msg':
                'ok',
            'data': [{
                'id': '234',
                'username': 'admin',
                'first_name': 'Ming',
                'last_name': 'Li',
            }]
        })

  def test_show_user_by_id(self):
    response = self.client.get("/users/234")
    self.assertEqual(response.status_code, 404)
    # self.assertEqual(response.json, {'data': [], 'msg': 'ok'})
    pass
