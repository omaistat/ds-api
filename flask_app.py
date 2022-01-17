from flask import Flask, request, jsonify
import joblib
import traceback
import pandas as pd
import numpy as np
import os


app = Flask(__name__)
app.config["DEBUG"] = True

@app.route("/")
def hello_world():
    return "<p>Hello Techie!</p>"

module_dir = os.path.abspath(os.path.dirname(__file__))
file_path = os.path.join(module_dir, "cleaned_data_num.csv")
df_raw = pd.read_csv(file_path)

df = df_raw.set_index('id').drop(columns = 'breed')
cats = df.iloc[:, :18]
# a series with cats' IDs to connect to prediction later
cats_ids = pd.Series(df.index)

module_dir = os.path.abspath(os.path.dirname(__file__))
file_path = os.path.join(module_dir, "cats_num_sample _100.csv")
cats_website = pd.read_csv(file_path)
cats_website = cats_website.drop(columns = 'Other (please specify).1')
cats_website.columns = ['id','cat_age', 'cat_gender', 'needs_outdoor', 'medical_conditions', 'behavioural_problems', 'cat_weight', 'likes_to_explore', 'playful', 'vocal', 'picked_up', 'timid', 'aggressive', 'adapts_quickly', 'prefers_alone', 'likes_stroke', 'tolerant_handled', 'friendly', 'fearful']

module_dir = os.path.abspath(os.path.dirname(__file__))
file_path = os.path.join(module_dir, "model.pkl")
lr = joblib.load(file_path) # Load "model.pkl"

module_dir = os.path.abspath(os.path.dirname(__file__))
file_path = os.path.join(module_dir, "model_columns.pkl")
model_columns = joblib.load(file_path)

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
            output = pd.DataFrame(prediction).sort_values(by = 0, ascending = False).iloc[:11].drop(columns = 0).reset_index().to_json()
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

