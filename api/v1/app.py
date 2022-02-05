#!/usr/bin/python3
"""module that starts a flask dev server"""
from models import storage
from flask import Flask
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    storage.close()


if __name__ == "__main__":
    """
    I need to run app.run() with host=HBNB_API_HOST
    and port=HBNB_API_PORT
    and threaded=True
    if the HOST env variable doesn't exist I need to use 0.0.0.0
    if the PORT env variable doesn exist I need to use port 5000
    """
    app.run(host="0.0.0.0", port="5000", threaded=True)
