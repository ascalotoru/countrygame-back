from flask import Flask, jsonify
import json
import random

app = Flask(__name__)


@app.route("/")
def index():
    return jsonify({"hello": "world"})


@app.route("/getcountries")
def get_countries():
    with open("resource/countries.json") as f:
        data = json.loads(f.read())
    return jsonify(data)


@app.route("/getrandomcountry")
def get_random_country():
    with open("resource/countries.json") as f:
        data = json.loads(f.read())
    max = len(data)
    return jsonify(data[random.randint(0, max)])


if __name__ == "__main__":
    app.run()
