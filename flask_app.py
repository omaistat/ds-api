from flask import Flask, Response, request, jsonify
import pandas as pd
import os
import json
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import joblib

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route("/")
def hello_techies():
    return "<p>Hello from TechLabs!</p>"
   
module_dir = os.path.abspath(os.path.dirname(__file__))
file_path = os.path.join(module_dir, "cleaned_data_num.csv")
df_raw = pd.read_csv(file_path)

@app.route("/raw_data/json", methods=["GET"])
def return_json():
    return Response(df_raw.to_json(orient="index"), mimetype="application/json")

@app.route("/api/id", methods=["GET"])
def get_line_by_id():
    if "id" in request.args:
        id = int(request.args["id"])
    else:
        return "Error: No id field provided. Please specify an id."

    results = []
    for i in df:
        if df["id"] == id:
            results.append(i)
    return jsonify(results)
    return Response(row.to_json(orient="index"), mimetype="application/json")
