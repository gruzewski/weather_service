from flask import Flask
import urllib3

app = Flask(__name__)
app.config.from_object('config')

if not app.debug:
    import logging
    from logging import FileHandler, Formatter
    log_file = FileHandler(app.config['LOG_FILE'])
    log_file.setFormatter(Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    log_file.setLevel(logging.WARNING)
    app.logger.addHandler(log_file)

url = app.config['WEATHER_API_URL']
api_key = app.config['WEATHER_API_KEY']


@app.route('/')
def hello():
    return "Hello World!"


@app.route('/api/v1.0/<string:city>/<int:period>')
def api(city, period):
    url2 = "http://%sq=%s&type=like&mode=json&APPID=%s" % (url, city, api_key)
    print url2
    http = urllib3.PoolManager()
    response = http.request('GET', url2)

    return response.data


if __name__ == "__main__":
    app.run()
