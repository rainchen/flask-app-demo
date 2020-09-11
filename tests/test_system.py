# from tests.base_test import app, config
# from flask_testing import TestCase, LiveServerTestCase
# import unittest

# # Tips: run this case test only: python -m unittest tests/test_system.py
# @unittest.skip('Not work with flask test') 
# class SkipTestSystem(TestCase, LiveServerTestCase):

#     def create_app(self):
#         # Set to 0 to have the OS pick the port.
#         app.config['LIVESERVER_PORT'] = 0
#         # Default timeout is 5 seconds
#         app.config['LIVESERVER_TIMEOUT'] = 10
#         return app

#     def test_server_is_up_and_running(self):
#         response = self.client.get(self.get_server_url())
#         self.assertEqual(response.status_code, 404)
