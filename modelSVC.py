from sklearn.svm import SVC
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

C = par.iloc[0,0]
kernel = par.iloc[0,1]

model = SVC(C= C,kernel= kernel)
model.fit(data,Labels)
            


joblib.dump(model,"modelo.joblib")