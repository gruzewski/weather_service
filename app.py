from flask import Flask, jsonify
from lib.provider.openweathermap import Openweathermap

app = Flask(__name__)
app.config.from_object('config')
provider = Openweathermap(app.config['PROVIDER']['OPENWEATHERMAP'])

if not app.debug:
    import logging
    from logging import FileHandler, Formatter
    log_file = FileHandler(app.config['LOG_FILE'])
    log_file.setFormatter(Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    log_file.setLevel(logging.WARNING)
    app.logger.addHandler(log_file)


@app.route('/')
def hello():
    return "Hello World!"


@app.route('/api/v1.0/<string:city>')
@app.route('/api/v1.0/<string:city>/<int:period>')
def api(city, period=1):
    response = provider.get_daily_forecast(city, period)

    return jsonify(response)


if __name__ == "__main__":
    app.run()
