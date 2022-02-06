#!/usr/bin/python3
"""
module that has routes to root and other endpoints
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.state import State
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route("/status", strict_slashes=False)
def status_code():
    data = {"status": "OK"}
    return jsonify(data)


@app_views.route("/stats", strict_slashes=False)
def count_all():
    data = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
    }
    return jsonify(data)
