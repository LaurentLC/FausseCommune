"""
Ce fichier a pour vocation d'être, en attendant mieux, l'entry point de CF pour faire tourner le "back" (la partie logique)
"""

import os

from flask import Flask

from back.data_interfaces.storage import StorageClient

app = Flask(__name__)


@app.route("/")
def hello_world():
    """Example Hello World route."""
    name = os.environ.get("NAME", "World")
    return f"Hello {name}!"


@app.route("/bucket")
def get_anything_from_bucket():
    """Just to test if auth works"""
    return StorageClient.download_string_file("gs://fausses_communes_bucket/fonctionne.txt")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
