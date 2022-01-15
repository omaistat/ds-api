from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route("/")
def hello_techies():
    return "<p>Hello from TechLabs!</p>"
    
df_raw = pd.read_csv('https://github.com/omaistat/ds-api/blob/a95d8e17d01dea724d8d7b06a05ec11ad2846adb/cats_num_sample%20_100.csv')

@app.route("/raw_data/all", methods=["GET"])
def return_all():
    return jsonify(df_raw)
