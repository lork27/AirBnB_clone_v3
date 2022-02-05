#!/usr/bin/python3
"""module that starts a flask dev server"""
from sqlalchemy import except_all
from models import storage
from flask import Flask, jsonify, safe_join
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    try:
        host = getenv("HBNB_API_HOST")
    except:
        host = "0.0.0.0"
    try:
        port = getenv("HBNB_API_PORT")
    except:
        port = "5000"
    app.run(host=host, port=port, threaded=True)
