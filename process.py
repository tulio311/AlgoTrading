import os
import pandas as pd
import sqlite3

con = sqlite3.connect("Algo.db",isolation_level=None)
cur = con.cursor()

takeProfit = 0.002

n = 36

X = pd.read_csv("criptos.csv")
X = X.iloc[-(n+1):-1,:].reset_index().drop(labels="index",axis=1)
X['max'] = {}
X['change'] = {}
X['labels'] = {}

def cerosyunos(p):
    if p:
        return 1
    else:
        return 0


for i in range(n-6):
    max = X.iloc[i+1:i+7,0].max()
    X['max'][i] = max

print(X)
X = X.iloc[:-6,:]

X['max'] = pd.to_numeric(X['max'])
X['btc'] = pd.to_numeric(X['btc'])


X['change'] = (X['max'] / X['btc'] ) - 1
X['labels'] = (X['change'] >= takeProfit).map(cerosyunos)
X = X.loc[:,['btc','eth','bch','xrp','labels']]

for i in range(n-6):
    query = "INSERT INTO training VALUES ("+str(X.iloc[i,0])+","+str(X.iloc[i,1])+","+str(X.iloc[i,2])+","+str(X.iloc[i,3])+","+str(X.iloc[i,4])+");"
    print(query)
    cur.execute(query)


    

