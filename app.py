from flask import Flask
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST, Histogram
import time

#http://localhost:5000
#http://localhost:5000/metrics
#http://localhost:9090


app = Flask(__name__)

# metric name: http_requests_total
# metric description: # of HTTP requests
requestCounter = Counter('http_requests_total', '# of HTTP requests')
requestLatency = Histogram('http_request_latency_seconds', 'Request latency in seconds')

@app.route("/")
def index():
    start_time = time.time()
    time.sleep(0.2)

    # Counter goes up everytime website is acsessed
    requestCounter.inc()
    
    latency = time.time() - start_time
    requestLatency.observe(latency)

    return (
        f"Total # of requests: {int(requestCounter._value.get())}" +
        "<br>" +
        f"Last request latency: {latency:.3f} seconds"
    )

@app.route("/metrics")
def metrics():
    # Return the metrics in a Prometheus-compatible format
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    # Runnign on http://localhost:5000/
    app.run(host="0.0.0.0", port=5000)
