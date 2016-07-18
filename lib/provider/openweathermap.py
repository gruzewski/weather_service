import urllib3
import json
from datetime import datetime

CITY = 'city'
DATE = 'dt'
HUMIDITY = 'humidity'
MAX = 'max'
MIN = 'min'
TEMP = 'temp'


class Openweathermap:
    def __init__(self, config, mode='json', units='metric'):
        self.api_key = config['API_KEY']
        self.base_url = config['BASE_URL']
        self.pool_manager = urllib3.PoolManager()
        self.mode = mode
        self.units = units


    def get_daily_forecast(self, city, period=1):
        url = '%s/forecast/daily?q=%s&type=like&mode=%s&units=%s&cnt=%s&APPID=%s' % (self.base_url, city, self.mode,
                                                                                     self.units, period, self.api_key)

        response = self.pool_manager.urlopen('GET', url)

        return self._build_response(response)


    @staticmethod
    def _build_response(response):
        # Documentation: http://openweathermap.org/forecast16#parameter
        original_response = json.loads(response.data)
        city = original_response[CITY]
        new_response = {
            'city': city['name'],
            'country': city['country'],
            'forecast': [{'avg': (day[TEMP][MAX] + day[TEMP][MIN]) / 2,
                          'date': Openweathermap._convert_time(day[DATE]),
                          'humidity': day[HUMIDITY],
                          'median': (day[TEMP][MAX] + day[TEMP][MIN]) / 2,
                          'max': day[TEMP][MAX],
                          'min': day[TEMP][MIN]
                          } for day in original_response['list']],
        }

        return new_response


    @staticmethod
    def _convert_time(unix_time):
        normal_time = datetime.fromtimestamp(int(unix_time)).strftime('%Y-%m-%d')

        return normal_time
