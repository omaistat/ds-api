from flask import Flask, request, jsonify
import joblib
import traceback
import pandas as pd
import numpy as np
import os
import json

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['JSON_SORT_KEYS'] = False

@app.route("/")
def hello_world():
    return "<p>Hello Techie!</p>"

module_dir = os.path.abspath(os.path.dirname(__file__))
file_path_1 = os.path.join(module_dir, "cleaned_data_num.csv")
df_raw = pd.read_csv(file_path_1)

file_path_2 = os.path.join(module_dir, "model.pkl")
lr = joblib.load(file_path_2) # Load "model.pkl"

file_path_3 = os.path.join(module_dir, "model_columns.pkl")
model_columns = joblib.load(file_path_3)

file_path_4 = os.path.join(module_dir, "cat_list_in_database.csv")
cats_website=pd.read_csv(file_path_4)

#cleaning df
df = df_raw.set_index('id').drop(columns = 'breed')

#cleaning cats data
cats_website = cats_website.drop(columns = 'breed')
cats_website.columns = ['id','cat_age',
                                                      'cat_gender',
                                                      'needs_outdoor',
                                                      'medical_conditions',
                                                      'behavioural_problems',
                                                      'cat_weight',
                                                      'likes_to_explore',
                                                      'playful',
                                                      'vocal',
                                                      'picked_up',
                                                      'timid',
                                                      'aggressive',
                                                      'adapts_quickly',
                                                      'prefers_alone',
                                                      'likes_stroke',
                                                      'tolerant_handled',
                                                      'friendly',
                                                      'fearful'
]




@app.route('/predict', methods=['GET', 'POST']) # Your API endpoint URL would consist /predict
def predict():
    if lr:
        try:
            json_ = request.json
            query = pd.DataFrame(json_)
            # extracting userID
            userID = query['userID'][0]
            userID_json = json.dumps(userID)
            #extracting user's answers
            query_data = pd.DataFrame(query['allUserAnswer'])
            query_data = query_data.reindex(columns=model_columns, fill_value=0)
            #test prediction
            #query = pd.DataFrame([[1,2,4,3,2,5,4,3,4,5,3,4,5,2,3,4,5,4,3]])
            query_data.columns = model_columns
            query_df = pd.DataFrame()
            query_new = query_df.append([query_data]*len(cats_website)).reset_index().drop(columns = ['index'])
            query_merged = pd.concat([cats_website, query_new], axis = 1, join='outer').set_index('id')
            prediction = pd.Series(lr.predict(query_merged))
            result = pd.DataFrame(prediction).sort_values(by = 0, ascending = False).iloc[:10].drop(columns = 0).reset_index()
            result.columns = ['catID']
            i = 1
            result_list = []
            for cat_id in result['catID']:
                case = {'catOrder': i, 'catID': cat_id}
                result_list.append(case.copy())
                i += 1
            #result_list.to_json()
            #return jsonify({'result': result})
            return jsonify({'userID': userID_json,
            		    'result': result_list})

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
