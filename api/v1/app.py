#!/usr/bin/python3
"""This is the start of RESTful api"""

from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage
import os


app = Flask(__name__)

app.register_blueprint(app_views, url_prefix="/api/v1")


@app.teardown_appcontext
def teardown_appcontext(exception):
    """the cleanup operation"""
    storage.close()


@app.errorhandler(404)
def errorhandler(error):
    """this is the handler for the 404 errors"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)