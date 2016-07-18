import app
import json
import re
import vcr
from unittest import TestCase
from mock import patch


def scrub_api_key(string, replacement=""):
    def before_record_response(response):
        response["headers"]["x-cache-key"] = re.sub(string, replacement, response["headers"]["x-cache-key"][0])
        return response
    return before_record_response


class AppUnitTest(TestCase):
    def setUp(self):
        self.app = app.app.test_client()
        self.city = "London"
        self.country = 'GB'
        self.period = 1
        self.expected_result = {"city": self.city, "country": self.country}


    def test_hello_world(self):
        response = self.app.get("/")
        assert "Hello World!" in response.data


    def test_blank_city(self):
        response = self.app.get("/api/v1.0/%s/%s" % ("", self.period))
        self.assertEquals(response.status_code, 404)


    @patch("app.provider")
    def test_blank_period(self, mock_provider):
        mock_provider.get_daily_forecast.return_value = self.expected_result
        response = self.app.get("/api/v1.0/%s" % self.city, follow_redirects=True)
        self.assertEquals(json.loads(response.data), self.expected_result)
        mock_provider.get_daily_forecast.assert_called_once_with(self.city, 1)


    @patch("app.provider")
    def test_7_days_period(self, mock_provider):
        mock_provider.get_daily_forecast.return_value = self.expected_result
        response = self.app.get("/api/v1.0/%s/%s" % (self.city, 7), follow_redirects=True)
        self.assertEquals(json.loads(response.data), self.expected_result)
        mock_provider.get_daily_forecast.assert_called_once_with(self.city, 7)


class AppIntegrationTest(TestCase):

    my_vcr = vcr.VCR(
        serializer="json",
        cassette_library_dir="fixtures/vcr_cassettes",
        record_mode="new_episodes",
        match_on=["uri", "method"],
        before_record_response=scrub_api_key("(?:APPID=)(.*?)&", "<api_key>"),
        filter_query_parameters=["APPID"],
    )

    def setUp(self):
        self.app = app.app.test_client()
        self.city = "London"
        self.period = 1


    def test_blank_period(self):
        response = self.app.get("/api/v1.0/%s" % self.city, follow_redirects=True)
        forecast = json.loads(response.data)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(forecast["forecast"]), 1)


    def test_7_days(self):
        response = self.app.get("/api/v1.0/%s/%s" % (self.city, 7))
        forecast = json.loads(response.data)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(forecast["forecast"]), 7)


    @my_vcr.use_cassette()
    def test_api_london(self):
        response = self.app.get("/api/v1.0/%s/%s" % (self.city, self.period))
        self.assertEquals(response.status_code, 200)
        assert '"city": "London"' in response.data
        assert '"country": "GB"' in response.data
        assert '"humidity": ' in response.data
