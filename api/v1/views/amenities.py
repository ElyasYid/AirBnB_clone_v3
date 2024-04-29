#!/usr/bin/python3
"""Tis module for api actions of amenities"""
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity

from flask import jsonify, abort, request


@app_views.route("/amenities")
def get_amenities():
    """Retrieve list of all amenity objects"""
    amenities = storage.all(Amenity)
    alll = []

    for amenity in amenities.values():
        alll.append(amenity.to_dict())

    return jsonify(alll)


@app_views.route("/amenities/<amenity_id>")
def get_amenity(amenity_id):
    """Retrieve one `Amenity`

    Args:
        amenity_id (str): Amenity identifier

    Returns:
        flask.Response: An amenity in json
    """
    the_amen = storage.get(Amenity, amenity_id)
    if not the_amen:
        abort(404)

    return jsonify(the_amen.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"])
def delete_amenity(amenity_id):
    """Delete an amenity.

    Args:
        amenity_id (str): amenity id

    Returns:
        dict: An empty JSON.

    Raises:
        404: amenity_id does not exist.
    """
    the_amen = storage.get(Amenity, amenity_id)
    if the_amen is None:
        abort(404)

    the_amen.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route("/amenities", methods=["POST"])
def create_amenity():
    """Create an amenity

    Returns:
        dict: New amenity in JSON

    Raises:
        400: If notvalid JSON/payload not contain key `name`
    """
    payload = request.get_json()
    if not payload:
        abort(400, "Not a JSON")
    if "name" not in payload:
        abort(400, "Missing name")

    the_amen = Amenity(**payload)
    the_amen.save()

    return jsonify(the_amen.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=["PUT"])
def update_amenity(amenity_id):
    """updates amenity based on id"""
    the_amen = storage.get(Amenity, amenity_id)
    payload = request.get_json()
    if not the_amen:
        abort(404)
    if not payload:
        abort(400, "Not a JSON")

    key = "name"
    setattr(the_amen, key, payload[key])
    the_amen.save()

    return jsonify(the_amen.to_dict()), 200
