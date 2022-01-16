# Dependencies
from flask import Flask, request, jsonify
import joblib
import traceback
import pandas as pd
import numpy as np

app = Flask(__name__)
df_raw = pd.read_csv('cleaned_data_num.csv')
df = df_raw.set_index('id').drop(columns = 'breed')
cats = df.iloc[:, :18]
@app.route('/predict', methods=['POST']) # Your API endpoint URL would consist /predict
def predict():
    if lr:
        try:
            json_ = request.json
            query = pd.DataFrame(json_)
            query = query.reindex(columns=model_columns, fill_value=0)
            query_merged = cats.merge(query, how = 'cross')
            prediction = list(LR.predict(query_merged))
            return jsonify({'prediction': prediction})

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
