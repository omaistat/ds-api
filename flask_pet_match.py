from flask import Flask, Response
import pandas as pd
import os
import json
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route("/")
def hello_techies():
    return "<p>Hello from TechLabs!</p>"
   
#module_dir = os.path.abspath(os.path.dirname(__file__))
#file_path = os.path.join(module_dir, "cleaned_data_num.csv")
df_raw = pd.read_excel('https://github.com/TechLabs-Berlin/wt21-pet-match/blob/main/data_set/data_cleaned/all_cleaned_num.xlsx?raw=true')

@app.route("/raw_data/json", methods=["GET"])
def return_json():
    return Response(df_raw.to_json(orient="index"), mimetype="application/json")
    
# Model


