import unittest

import requests
from flask_testing import LiveServerTestCase, TestCase

from tests.base_test import app


# FIXME: make this can work with `flask test`, currently run this case test have to use: python -m unittest tests/skip_test_liveserver.py
# @unittest.skip('Not work with flask test')
class TestLiveserver(TestCase, LiveServerTestCase):

  def create_app(self):
    # app.config['TESTING'] = True
    # Set to 0 to have the OS pick the port.
    # FIXME: Failed to start the server after 5 seconds. is triggered when setting LIVESERVER_PORT to 0
    # refs: https://github.com/jarus/flask-testing/issues/155
    app.config['LIVESERVER_PORT'] = 6000
    # Default timeout is 5 seconds
    app.config['LIVESERVER_TIMEOUT'] = 10
    return app

  def test_server_is_up_and_running(self):
    root_url = self.get_server_url()

    # request root url
    response = requests.get(root_url)
    self.assertEqual(response.status_code, 404)

    # request static file
    response = requests.get(root_url + "/static/flask-logo.png")
    self.assertEqual(response.status_code, 200)

    # request dynamic data
    # before step: pipenv run env FLASK_ENV=testing flask db upgrade
    response = requests.get(root_url + "/users")
    self.assertEqual(response.status_code, 200)
