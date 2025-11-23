"""
Ce fichier a pour vocation d'être, en attendant mieux, l'entry point de CF pour faire tourner le "back" (la partie logique)
"""

import os
import time

from flask import Flask, request

from back.data_interfaces.storage import StorageClient
from back.markov.multi_prediction import generate_name

app = Flask(__name__)


@app.route("/")
def hello_world():
    """Example Hello World route."""
    name = os.environ.get("NAME", "World")
    return f"Hello {name}!"


@app.route("/api/generate_name", methods=['POST'])
def generate_name():
    data = request.get_json()
    lat = data['lat']
    long = data['long']
    return generate_name(lat, long)



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
