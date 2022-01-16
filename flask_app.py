import os
import json
from flask import Flask, jsonify, request, Response
import pandas as pd

app = Flask(__name__)
app.config["DEBUG"] = True

wines = [
    {"id": 0, "alcohol": 8, "quality": 10},
    {"id": 1, "alcohol": 12, "quality": 8},
    {"id": 2, "alcohol": 10.5, "quality": 9},
]

module_dir = os.path.abspath(os.path.dirname(__file__))
file_path = os.path.join(module_dir, "winequality-white.csv")
df = pd.read_csv(file_path, sep=";")


@app.route("/")
def hello_world():
    return "<p>Hello, from TechLabs!</p>"


@app.route("/api/wines/all", methods=["GET"])
def return_all():
    return Response(df.to_json(orient="index"), mimetype="application/json")


@app.route("/api/wines", methods=["GET"])
def get_wine_by_id():
    if "id" in request.args:
        id = int(request.args["id"])
    else:
        return "Error: No id field provided. Please specify an id."

    row = df.iloc[[id]]
    return Response(row.to_json(orient="index"), mimetype="application/json")


@app.route("/api/wines/filter", methods=["GET"])
def filter_wines():
    requested_quality = request.args.get("quality")
    if requested_quality:
        filtered_data = df[df.quality == int(requested_quality)]
        return Response(
            filtered_data.to_json(orient="index"), mimetype="application/json"
        )
    return []
