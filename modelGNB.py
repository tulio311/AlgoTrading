from sklearn.naive_bayes import GaussianNB
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

data = X.iloc[5:,:4]
Labels = X.iloc[5:,4]


print(data)
print(Labels)

model = GaussianNB()

model.fit(data,Labels)


joblib.dump(model,"modelo.joblib")