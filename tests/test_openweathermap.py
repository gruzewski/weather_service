from lib.provider.openweathermap import Openweathermap as OWM
from mock import MagicMock
from unittest import TestCase
from collections import namedtuple


HUMIDITY = 71
MAX = 24.11
MIN = 14.86
AVG = (MAX + MIN) / 2
MEDIAN = AVG


class OpenweathermapUnitTest(TestCase):

    def setUp(self):
        Response = namedtuple('Response', ['data'])

        with open("fixtures/openweathermap_response.json") as response_file:
            response_json = response_file.read()

        self.api_key = "12345"
        self.base_url = "http://example.com/api/v1.0"
        self.config = {"API_KEY": self.api_key, "BASE_URL": self.base_url}
        self.city = "London"
        self.country = "GB"
        self.mode = "json"
        self.units = "metric"
        self.normal_date = "2016-07-17"
        self.response = Response(response_json)
        self.expected_result = {
            "city": self.city,
            "country": self.country,
            "forecast": [{"avg": AVG,
                          "date": self.normal_date,
                          "humidity": HUMIDITY,
                          "median": MEDIAN,
                          "max": MAX,
                          "min": MIN
                          }],
        }
        self.owm = OWM(self.config, mode=self.mode, units=self.units)
        self.owm.pool_manager = MagicMock()


    def test_owm_object(self):
        self.assertEquals(self.owm.api_key, self.api_key)
        self.assertEquals(self.owm.base_url, self.base_url)
        self.assertEquals(self.mode, self.mode)


    def test_get_daily_forecast(self):
        self.owm.pool_manager.urlopen.return_value = self.response
        actual_response = self.owm.get_daily_forecast(self.city, 1)
        self.assertEquals(actual_response, self.expected_result)
