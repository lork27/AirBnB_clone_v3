#!/usr/bin/python3
"""
module that handles alll CRUD actions for user objects
"""
from flask import abort, request, jsonify
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route("/users", strict_slashes=False)
def all_users():
    '''
    returns json of User objects
    '''
    users = storage.all(User).values()
    users_list = []
    for obj in users:
        users_list.append(obj.to_dict())

    return jsonify(users_list)


@app_views.route("/users/<id>", strict_slashes=False,
                 methods=["GET", "DELETE"])
def user_by_id(id=None):
    '''
    returns json of User objects
    '''
    user = storage.get(User, id)
    if user is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(user.to_dict())
    if request.method == 'DELETE':
        storage.delete(user)
        storage.save()
        return jsonify({}), 200


@app_views.route("/users", strict_slashes=False, methods=["POST"])
def post_user():
    '''
    returns json of User objects
    '''
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        if "email" not in json:
            abort(400, description="Missing email")
        if "password" not in json:
            abort(400, description="Missing password")
        new_user = User(email=json["email"], password=json["password"])
        storage.new(new_user)
        storage.save()
        return jsonify(new_user.to_dict()), 201
    else:
        abort(400, description="Not a JSON")


@app_views.route("/users/<id>", strict_slashes=False, methods=["PUT"])
def update_user(id):
    '''
    returns json of User objects
    '''

    user = storage.get(User, id)
    if user is None:
        abort(404)
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        for key, value in json.items():
            if key not in ["id", "email", "created_at", "updated_at"]:
                setattr(user, key, value)
        storage.save()
        return jsonify(user.to_dict()), 200
    else:
        abort(400, description="Not a JSON")
