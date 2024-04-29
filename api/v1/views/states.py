#!/usr/bin/python3
"""Defines the api actions for state objects"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route("/states", methods=['GET'])
def get_states():
    """Gets the list of all `State` objects"""
    listt = []
    for value in storage.all(State).values():
        listt.append(value.to_dict())
    return jsonify(listt)


@app_views.route("/states/<state_id>", methods=['GET'])
def get_one_state(state_id: str):
    """Gets one state object

    Args:
        state_id (string): state id

    Returns:
        `State` object in json
    """
    one_state = storage.get(State, state_id)
    if one_state is None:
        abort(404)
    return jsonify(one_state.to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"])
def remove_state(state_id):
    """removes a state object

    Args:
        state_id (str): state id

    Returns:
        Empty dictionary - `{}`
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/states", methods=["POST"])
def make_state():
    """Creates a State object"""
    if not request.get_json():
        abort(400, "Not a JSON")
    if "name" not in request.get_json():
        abort(400, "Missing name")
    state = State(**request.get_json())
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["PUT"])
def update_state(state_id):
    """Updates State

    Args:
        state_id (str): state identifier

    Returns:
        State object with status code 200
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    key = "name"
    setattr(state, key, request.get_json().get(key))
    state.save()
    return jsonify(state.to_dict()), 200
