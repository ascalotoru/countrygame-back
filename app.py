from flask import Flask, jsonify, request
from geopy import distance
import json
import random

app = Flask(__name__)


@app.route("/")
def index():
    return jsonify({"hello": "world"})


@app.route("/getcountries", methods=["GET"])
def get_countries():
    with open("resource/countries.json") as f:
        data = json.loads(f.read())
    return jsonify(data)


@app.route("/getrandomcountry", methods=["GET"])
def get_random_country():
    with open("resource/countries.json") as f:
        data = json.loads(f.read())
    max = len(data)
    return jsonify(data[random.randint(0, max)])


@app.route("/check", methods=["POST"])
def check_result():
    with open("resource/countries.json") as f:
        data = json.loads(f.read())
    r = json.loads(request.data)
    country = r["country"]
    capital = r["capital"]
    for d in data:
        if d["name"]["common"] == country:
            solution_country = d
            break
    for d in data:
        if len(d["capital"]) == 0:
            continue
        if d["name"]["common"] == country and d["capital"][0] == capital:
            return jsonify({"solved": True})
        if d["capital"][0] == capital:
            player_country = d
            dist = get_distance(solution_country=solution_country,
                                player_country=player_country)
            return jsonify({"solved": False, "distance": int(dist)})


def get_distance(solution_country=None, player_country=None):
    solution_country_latlng = (solution_country["latlng"][0],
                               solution_country["latlng"][1])
    player_country_latlng = (player_country["latlng"][0],
                             player_country["latlng"][1])
    return distance.distance(player_country_latlng, solution_country_latlng).km


if __name__ == "__main__":
    app.run()
