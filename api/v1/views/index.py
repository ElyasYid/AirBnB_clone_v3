#!/usr/bin/python3
"""This views index containing status and endpoints"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def status():
    """this is the status of the api"""
    return jsonify({"status": "OK"})
