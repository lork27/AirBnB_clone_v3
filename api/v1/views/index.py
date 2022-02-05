#!/usr/bin/python3
"""
module that has routes to root and other endpoints
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status", strict_slashes=False)
def status_code():
    data = {"status": "ok"}
    return jsonify(data)
