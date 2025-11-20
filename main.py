"""
Ce fichier a pour vocation d'être, en attendant mieux, l'entry point de CF pour faire tourner le "back" (la partie logique)
"""

import os

from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    """Example Hello World route."""
    name = os.environ.get("NAME", "World")
    return f"Hello {name}!"

# TODO creer une vraie route back pour aller au bout de l'exercice (qui ait besoin du storage pour tester l'auth)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))