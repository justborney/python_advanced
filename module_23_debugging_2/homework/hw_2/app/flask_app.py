import time
import random

from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)


@app.route('/homework')
@metrics.counter('requests_counter',
                 'count the number of requests')
def homework():
    time.sleep(random.random() * 0.4)
    return 'ok'


if __name__ == '__main__':
    app.run('0.0.0.0', 5000, threaded=True)
