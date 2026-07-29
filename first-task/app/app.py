"""
Simple API application for the DevOps task.
Exposes:
  GET /          -> basic info
  GET /health    -> health check (used by Docker HEALTHCHECK and the monitor script)
  GET /metrics   -> request count + uptime (used by the dashboard)
"""
from flask import Flask, jsonify
import time

app = Flask(__name__)
from flask_cors import CORS
CORS(app)   

START_TIME = time.time()
REQUEST_COUNT = 0


@app.before_request
def _count_request():
    global REQUEST_COUNT
    REQUEST_COUNT += 1


def _uptime_seconds() -> float:
    return round(time.time() - START_TIME, 2)


@app.route("/")
def home():
    return jsonify({
        "message": "API is running",
        "uptime_seconds": _uptime_seconds(),
    })


@app.route("/health")
def health():
    # Kept intentionally simple/fast: no external dependency checks here.
    # Extend this with DB/cache pings if the real app has dependencies.
    return jsonify({
        "status": "healthy",
        "uptime_seconds": _uptime_seconds(),
    }), 200


@app.route("/metrics")
def metrics():
    return jsonify({
        "request_count": REQUEST_COUNT,
        "uptime_seconds": _uptime_seconds(),
    })


if __name__ == "__main__":
   app.run(host="0.0.0.0", port=5000)

