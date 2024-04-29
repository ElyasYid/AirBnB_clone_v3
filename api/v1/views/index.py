#!/usr/bin/python3
"""This views index containing status and endpoints"""

from api.v1.views import app_views
from flask import jsonify
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage


classes = {
    "amenities": Amenity,
    "cities": City,
    "places": Place,
    "reviews": Review,
    "states": State,
    "users": User,
}


@app_views.route('/status', methods=['GET'])
def status():
    """this is the status of the api"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", methods=['GET'])
def stats():
    """this retrieves number of objects by type"""
    total = {}

    for key, value in classes.items():
        total[key] = storage.count(value)

    return jsonify(total)
