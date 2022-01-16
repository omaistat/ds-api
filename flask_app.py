# Dependencies
from flask import Flask, request, jsonify
import joblib
import traceback
import pandas as pd
import numpy as np


app = Flask(__name__)
app.config["DEBUG"] = True

df_raw = pd.read_csv('cleaned_data_num.csv')
df = df_raw.set_index('id').drop(columns = 'breed')
cats = df.iloc[:, :18]
# a series with cats' IDs to connect to prediction later
cats_ids = pd.Series(df.index)

@app.route("/")
def hello_world():
    return "<p>Hello Techie!</p>"

@app.route('/predict', methods=['GET', 'POST']) # Your API endpoint URL would consist /predict
def predict():
    if lr:
        try:
            json_ = request.json
            query = pd.DataFrame(json_)
            query = query.reindex(columns=model_columns, fill_value=0)
            #test prediction
            #query = pd.DataFrame([[1,2,4,3,2,5,4,3,4,5,3,4,5,2,3,4,5,4,3]])
            query.columns = model_columns
            query_merged = cats.merge(query, how = 'cross')
            prediction = pd.Series(lr.predict(query_merged))
            output = pd.concat([cats_ids, prediction], axis = 1).set_index('id').to_json()
            return jsonify({'output': output})

        except:

            return jsonify({'trace': traceback.format_exc()})
    else:
        print ('Train the model first')
        return ('No model here to use')

if __name__ == '__main__':
    try:
        port = int(sys.argv[1]) # This is for a command-line input
    except:
        port = 12345 # If you don't provide any port the port will be set to 12345

    lr = joblib.load("model.pkl") # Load "model.pkl"
    print ('Model loaded')
    model_columns = joblib.load("model_columns.pkl") # Load "model_columns.pkl"
    print ('Model columns loaded')

    app.run(port=port, debug=True)
