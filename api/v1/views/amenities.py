#!/usr/bin/python3
"""
module that handles alll CRUD actions for amenity objects
"""
from flask import abort, request, jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", strict_slashes=False)
def all_amenities():
    '''
    returns json of Amenity objects
    '''
    amenities = storage.all(Amenity).values()
    amenities_list = []
    for obj in amenities:
        amenities_list.append(obj.to_dict())

    return jsonify(amenities_list)


@app_views.route("/amenities/<id>", strict_slashes=False,
                 methods=["GET", "DELETE"])
def amenity_by_id(id=None):
    '''
    returns json of Amenity objects
    '''
    amenity = storage.get(Amenity, id)
    if amenity is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(amenity.to_dict())
    if request.method == 'DELETE':
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200


@app_views.route("/amenities", strict_slashes=False, methods=["POST"])
def post_amenity():
    '''
    returns json of Amenity objects
    '''
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        if "name" not in json:
            abort(400, description="Missing name")
        new_amenity = Amenity(name=json["name"])
        storage.new(new_amenity)
        storage.save()
        return jsonify(new_amenity.to_dict()), 201
    else:
        abort(400, description="Not a JSON")


@app_views.route("/amenities/<id>", strict_slashes=False, methods=["PUT"])
def update_amenity(id):
    '''
    returns json of Amenity objects
    '''

    amenity = storage.get(Amenity, id)
    if amenity is None:
        abort(404)
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        if "name" not in json:
            abort(400, description="Missing name")
        for key, value in json.items():
            setattr(amenity, key, value)
        storage.save()
        return jsonify(amenity.to_dict()), 200
    else:
        abort(400, description="Not a JSON")
