
from flask import Flask, redirect, url_for, request, render_template, jsonify
from libmomgo import mongo_lib
from markupsafe import escape
from libtool import json_encoder

import http

app = Flask(__name__)


@app.route("/pokemon/<region>/<number>", methods=["GET"])
def find_pokemon(region, number):
    items = mongo_lib.find_one(region=region, number=number)

    return json_encoder.JSONEncoder().encode(items)


@app.route("/pokemon", methods=["POST"])
def insert_pokemon():
    pokemon_item = {
        "number": request.json["number"],
        "name": request.json["name"],
        "types": request.json["types"],
        "region": request.json["region"],
        "evolution": request.json["evolution"],
    }
    mongo_lib.insert(pokemon_item)

    return json_encoder.JSONEncoder().encode(pokemon_item)


@app.route("/pokemons", methods=["POST"])
def find_pokemons():
    pokemon_item = request.json["types"]
    pokemons = mongo_lib.find_many(pokemon_item)

    return json_encoder.JSONEncoder().encode(pokemons)


@app.route("/pokemon/<region>/<number>", methods=["PUT"])
def update_pokemon(region, number):
    evolutions: list = request.json["evolutions"]
    pokemons = mongo_lib.update(region=region, number=number, evolutions=evolutions)
    return  json_encoder.JSONEncoder().encode(pokemons)


@app.route("/pokemon/<region>/<number>", methods=["DELETE"])
def delete_pokemon(region, number):
    mongo_lib.delete_one(region=region, number=number)
    return  "", http.HTTPStatus.NO_CONTENT

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)