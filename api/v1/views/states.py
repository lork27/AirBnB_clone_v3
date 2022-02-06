#!/usr/bin/python3
"""
module that handles alll CRUD actions for state objects
"""
from flask import abort, request, jsonify
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route("/states", strict_slashes=False)
def all_states():
    '''
    returns json of State objects
    '''
    states = storage.all(State).values()
    states_list = []
    for obj in states:
        states_list.append(obj.to_dict())

    return jsonify(states_list)


@app_views.route("/states/<id>", strict_slashes=False,
                 methods=["GET", "DELETE"])
def state_by_id(id=None):
    '''
    returns json of State objects
    '''
    state = storage.get(State, id)
    if state is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(state.to_dict())
    if request.method == 'DELETE':
        storage.delete(state)
        storage.save()
        return jsonify({}), 200


@app_views.route("/states", strict_slashes=False, methods=["POST"])
def post_state():
    '''
    returns json of State objects
    '''
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        if "name" not in json:
            abort(400, description="Missing name")
        new_state = State(name=json["name"])
        storage.new(new_state)
        storage.save()
        return jsonify(new_state.to_dict()), 201
    else:
        abort(400, description="Not a Json")


@app_views.route("/states/<id>", strict_slashes=False, methods=["PUT"])
def update_state(id):
    '''
    returns json of State objects
    '''

    state = storage.get(State, id)
    if state is None:
        abort(404)
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        if "name" not in json:
            abort(400, description="Missing name")
        for key, value in json.items():
            setattr(state, key, value)
        storage.save()
        return jsonify(state.to_dict()), 201
    else:
        abort(400, description="Not a Json")
