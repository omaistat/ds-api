from flask import Flask, jsonify, Response
import pandas as pd

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route("/")
def hello_techies():
    return "<p>Hello from TechLabs!</p>"
    
df_raw = pd.read_excel('https://github.com/TechLabs-Berlin/wt21-pet-match/blob/main/data_set/data_cleaned/all_cleaned_num.xlsx?raw=true')

@app.route("/raw_data/all", methods=["GET"])
def return_all():
    return Response(df_raw.to_json(orient="index"), mimetype="application/json")
