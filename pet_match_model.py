import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

df_raw = pd.read_excel('https://github.com/TechLabs-Berlin/wt21-pet-match/blob/main/data_set/data_cleaned/all_cleaned_num.xlsx?raw=true')

# MODEL
#df = df_raw.drop(columns = 'breed')
df = df_raw.set_index('id').drop(columns = 'breed')
X = df.iloc[:, :37]
y = df.iloc[:, 37]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=19)
LR = LinearRegression()
LR.fit(X_train,y_train)

joblib.dump(LR, 'model.pkl')
LR = joblib.load('model.pkl')

adopters = df.iloc[:, 18:37]
cats = df.iloc[:, :18]

# a series with cats' IDs to connect to prediction later
cats_ids = pd.Series(df.index)

model_columns = list(adopters.columns)
joblib.dump(model_columns, 'model_columns.pkl')
print("Models columns dumped!")
