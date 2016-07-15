import app
import flask
import unittest

class AppTestCase(unittest.TestCase):

    def setUp(self):
        # Create Flas test client
        self.app = app.app.test_client()

    def tearDown(self):
        # Clear data
        pass

    def test_hello_world(self):
        # Check main page
        response = self.app.get('/')
        assert 'Hello World!' in response.data