from flask import Flask
from prometheus_client import Counter, generate_latest
from prometheus_client import CONTENT_TYPE_LATEST
from flask import Response

app = Flask(__name__)

REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests')

@app.route("/")
def home():
    REQUEST_COUNT.inc()
    return "Hello, Prometheus!"

@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)