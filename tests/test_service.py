import app
import vcr
import unittest
import urllib2


class AppTestCase(unittest.TestCase):
    my_vcr = vcr.VCR(
        serializer='json',
        cassette_library_dir='fixtures/vcr_cassettes',
        record_mode='new_episodes',
        match_on=['uri', 'method'],
    )


    def setUp(self):
        # Create Flask test client
        self.app = app.app.test_client()
        self.city = "London"
        self.period = 3


    def test_hello_world(self):
        # Check main page
        response = self.app.get('/')
        assert 'Hello World!' in response.data


    @my_vcr.use_cassette()
    def test_api(self):
        response = self.app.get("/api/v1.0/London/%s" % self.period)
        self.assertEquals(response.status_code, 200)
        assert 'humidity' in response.data
