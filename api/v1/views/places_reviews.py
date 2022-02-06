#!/usr/bin/python3
"""
module that handles alll CRUD actions for review objects
"""
from flask import abort, request, jsonify
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route("/places/<id>/reviews", strict_slashes=False)
def all_reviews(id):
    '''
    returns json of Place objects
    '''
    place = storage.get(Place, id)
    if place is None:
        abort(404)
    reviews_list = []
    for review in place.reviews:
        reviews_list.append(review.to_dict())

    return jsonify(reviews_list)


@app_views.route("/reviews/<id>", strict_slashes=False,
                 methods=["GET", "DELETE"])
def review_by_id(id=None):
    '''
    returns json of Place objects
    '''
    review = storage.get(Review, id)
    if review is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(review.to_dict())
    if request.method == 'DELETE':
        storage.delete(review)
        storage.save()
        return jsonify({}), 200


@app_views.route("/places/<id>/reviews",
                 strict_slashes=False, methods=["POST"])
def post_review(id):
    '''
    returns json of Place objects
    '''
    place = storage.get(Place, id)
    if place is None:
        abort(404)
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json

        if "user_id" not in json:
            abort(400, description="Missing user_id")
        user = storage.get(User, json["user_id"])
        if user is None:
            abort(404)
        if "text" not in json:
            abort(400, description="Missing text")
        new_review = Review(user_id=user.id)
        new_review.place_id = place.id
        new_review.text = json["text"]
        storage.new(new_review)
        storage.save()
        return jsonify(new_review.to_dict()), 201
    else:
        abort(400, description="Not a JSON")


@app_views.route("/reviews/<id>", strict_slashes=False, methods=["PUT"])
def update_review(id):
    '''
    returns json of Place objects
    '''
    review = storage.get(Review, id)
    if review is None:
        abort(404)
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        if "name" not in json:
            abort(400, description="Missing name")
        for key, value in json.items():
            if key not in ["id", "user_id", "place_id", "created_at",
                           "updated_at"]:
                setattr(review, key, value)
        storage.save()
        return jsonify(review.to_dict()), 200
    else:
        abort(400, description="Not a JSON")
