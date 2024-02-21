import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
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
crit = par.iloc[0,1]


model = RandomForestClassifier(n_estimators=arb,criterion=crit)
model.fit(data,Labels)



joblib.dump(model,"modelo.joblib")

