from flask import Flask
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# metric name: http_requests_total
# metric description: # of HTTP requests
requestCounter = Counter('http_requests_total', '# of HTTP requests')

@app.route("/")
def index():
    # Counter goes up everytime website is acsessed
    requestCounter.inc()
    return f"Total # of requests: {int(requestCounter._value.get())}"

@app.route("/metrics")
def metrics():
    # Return the metrics in a Prometheus-compatible format
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    # Runnign on http://localhost:5000/
    app.run(host="0.0.0.0", port=5000)
