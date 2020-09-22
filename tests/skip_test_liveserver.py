from tests.base_test import app
from flask_testing import TestCase, LiveServerTestCase
import unittest
import requests


# FIXME: make this can work with `flask test`, currently run this case test have to use: python -m unittest tests/skip_test_liveserver.py
# @unittest.skip('Not work with flask test')
class TestLiveserver(TestCase, LiveServerTestCase):

    def create_app(self):
        # Set to 0 to have the OS pick the port.
        app.config['LIVESERVER_PORT'] = 0
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
