# Weather API service

Simple Weather RESTfull API service that takes city and time period and returns min, max, average, and median temperature
and humidity.

## Local setup

  Install all dependencies:

  ```
  wget https://bootstrap.pypa.io/get-pip.py && python get-pip.py
  pip install virtualenv
  virtualenv -p python3 weather_virtenv
  . weather_virtenv/bin/activate
  git clone git@github.com:gruzewski/weather_service.git
  cd weather_service
  pip install -r requirements.txt
  ```
  
  Next copy sample config and update API key:
  
  ```
  cp sample_config.py config.py
  vim config.py
  ```
  
  Finally run it:
  
  ```
  python app.py
  ```

## Testing
  
  To run all the tests:

  ```
  nosetests tests/
  ```
  
  I have used [vcrpy](https://github.com/kevin1024/vcrpy) to fake original weather api provider's response. If you 
  want to use another provider (or something has changed in the current API response) you can delete 
  `tests/fixtures/vcr_cassettes/test_api_london` and a new file will be created after the first run.