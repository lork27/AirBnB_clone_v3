#!/usr/bin/python3
"""
module that handles alll CRUD actions for city objects
"""
from flask import abort, request, jsonify
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route("/states/<id>/cities", strict_slashes=False)
def all_cities(id):
    '''
    returns json of City objects
    '''
    state = storage.get(State, id)
    if state is None:
        abort(404)
    cities_list = []
    for city in state.cities:
        cities_list.append(city.to_dict())

    return jsonify(cities_list)


@app_views.route("/cities/<id>", strict_slashes=False,
                 methods=["GET", "DELETE"])
def city_by_id(id=None):
    '''
    returns json of City objects
    '''
    city = storage.get(City, id)
    if city is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(city.to_dict())
    if request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return jsonify({}), 200


@app_views.route("/states/<id>/cities", strict_slashes=False, methods=["POST"])
def post_city(id):
    '''
    returns json of City objects
    '''
    state = storage.get(State, id)
    if state is None:
        abort(404)
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        if "name" not in json:
            abort(400, description="Missing name")
        new_city = City(name=json["name"], state_id=json["state_id"])
        storage.new(new_city)
        storage.save()
        return jsonify(new_city.to_dict()), 201
    else:
        abort(400, description="Not a JSON")


@app_views.route("/cities/<id>", strict_slashes=False, methods=["PUT"])
def update_city(id):
    '''
    returns json of City objects
    '''

    city = storage.get(City, id)
    if city is None:
        abort(404)
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        if "name" not in json:
            abort(400, description="Missing name")
        for key, value in json.items():
            setattr(city, key, value)
        storage.save()
        return jsonify(city.to_dict()), 200
    else:
        abort(400, description="Not a JSON")
