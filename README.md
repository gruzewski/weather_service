# Weather API service

Simple Weather RESTfull API service that takes city and time period and returns min, max, average, and median temperature
and humidity.

## Local setup

  ```
  wget https://bootstrap.pypa.io/get-pip.py && python get-pip.py
  pip install virtualenv
  virtualenv -p python3 weather_virtenv
  . weather_virtenv/bin/activate
  git clone git@github.com:gruzewski/weather_service.git
  cd weather_service
  pip install -r requirements.txt
  ```

## Testing