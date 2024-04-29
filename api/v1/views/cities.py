#!/usr/bin/python3
"""Tis handles of api for city objects"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City


@app_views.route("/states/<state_id>/cities")
def cities_in_a_state(state_id):
    """Retrieve the list of all `City` objects of a state

    Args:
        state_id (str): State identifier
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    endd = []
    for city in state.cities:
        endd.append(city.to_dict())

    return jsonify(endd)


@app_views.route("/cities/<city_id>")
def get_city(city_id):
    """Retrieve a `City`"""
    sty = storage.get(City, city_id)
    if not sty:
        abort(404)

    return jsonify(sty.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"])
def delete_city(city_id):
    """Remove a city

    Args:
        city_id (str): City identifier
    """
    sty = storage.get(City, city_id)
    if not sty:
        abort(404)

    sty.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities", methods=["POST"])
def create_city(state_id):
    """Create a city

    Args:
        state_id (str): State identifier
    """
    copse = storage.get(State, state_id)
    if not copse:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    if "name" not in request.get_json():
        abort(400, "Missing name")

    sty = City(state_id=state_id, **request.get_json())
    sty.save()

    return jsonify(sty.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"])
def update_city(city_id):
    sty = storage.get(City, city_id)
    if not sty:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")

    key = "name"
    setattr(sty, key, request.get_json().get(key))
    sty.save()

    return jsonify(sty.to_dict())
