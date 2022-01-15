from flask import Flask, Response
import pandas as pd
import os
import json

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route("/")
def hello_techies():
    return "<p>Hello from TechLabs!</p>"
   
module_dir = os.path.abspath(os.path.dirname(__file__))
file_path = os.path.join(module_dir, "cleaned_data_num.csv")
df_raw = pd.read_csv(file_path, sep=",")

@app.route("/raw_data/json", methods=["GET"])
def return_json():
    return Response(df_raw.to_json(orient="index"), mimetype="application/json")
