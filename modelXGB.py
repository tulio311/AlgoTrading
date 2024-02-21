from xgboost import XGBClassifier
import numpy as np
import pandas as pd
import joblib
import sqlite3

con = sqlite3.connect("Algo.db",isolation_level=None)
cur = con.cursor()

cota = "002"

# Training data extraction

# SQL
query = "SELECT * FROM training;"
print(query)
cur.execute(query)
x1 = cur.fetchall()
X = pd.DataFrame(x1,columns=['btc','eth','bch','xrp','labels'])

# CSV
#X = pd.read_csv("4criptoLabeled"+cota+".csv")

#----------------------------------------------------------

par = pd.read_csv("parametros.csv")

data = X.iloc[:,:4]
Labels = X.iloc[:,4]

arb = par.iloc[0,0]
eta = par.iloc[0,1]
prof = par.iloc[0,2]
gamma = par.iloc[0,3]

model = XGBClassifier(n_estimators=arb,objective='binary:logistic',eta=eta,
                      max_depth=prof,gamma = gamma,min_child_weight = 1,scale_pos_weight = 1)
model.fit(data,Labels)

joblib.dump(model,"modelo.joblib")
