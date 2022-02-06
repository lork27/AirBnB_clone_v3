#!/usr/bin/python3
"""
module that handles alll CRUD actions for place objects
"""
from flask import abort, request, jsonify
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route("/cities/<id>/places", strict_slashes=False)
def all_places(id):
    '''
    returns json of City objects
    '''
    city = storage.get(City, id)
    if city is None:
        abort(404)
    places_list = []
    for place in city.places:
        places_list.append(place.to_dict())

    return jsonify(places_list)


@app_views.route("/places/<id>", strict_slashes=False,
                 methods=["GET", "DELETE"])
def place_by_id(id=None):
    '''
    returns json of City objects
    '''
    place = storage.get(Place, id)
    if place is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(place.to_dict())
    if request.method == 'DELETE':
        storage.delete(place)
        storage.save()
        return jsonify({}), 200


@app_views.route("/cities/<id>/places", strict_slashes=False, methods=["POST"])
def post_place(id):
    '''
    returns json of City objects
    '''
    city = storage.get(City, id)
    if city is None:
        abort(404)
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json

        if "user_id" not in json:
            abort(400, description="Missing user_id")
        user = storage.get(User, id)
        if user is None:
            abort(404)
        if "name" not in json:
            abort(400, description="Missing name")
        new_place = Place(name=json["name"], user_id=user.id)
        storage.new(new_place)
        storage.save()
        return jsonify(new_place.to_dict()), 201
    else:
        abort(400, description="Not a JSON")


@app_views.route("/places/<id>", strict_slashes=False, methods=["PUT"])
def update_place(id):
    '''
    returns json of City objects
    '''

    place = storage.get(Place, id)
    if place is None:
        abort(404)
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        if "name" not in json:
            abort(400, description="Missing name")
        for key, value in json.items():
            setattr(place, key, value)
        storage.save()
        return jsonify(place.to_dict()), 200
    else:
        abort(400, description="Not a JSON")
