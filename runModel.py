import joblib
import numpy as np
from sklearn.naive_bayes import GaussianNB
import pandas as pd
import os
import time
import csv
from datetime import datetime
import sqlite3

con = sqlite3.connect("Algo.db",isolation_level=None)
cur = con.cursor()

os.system('cmd /c "node Prices.js"')

model = joblib.load("modelo.joblib")

takeProfit = .002



# Getting prices

# SQL
query = "SELECT * FROM PreciosNow;"
print(query)
cur.execute(query)
x1 = cur.fetchall()
x1 = pd.DataFrame(x1,columns=['btc','eth','bch','xrp'])

# CSV
#x1 = pd.read_csv("PreciosNow.csv")

#-------------------------------------


x = [[x1.iloc[0,0],x1.iloc[0,1],x1.iloc[0,2],x1.iloc[0,3]]]

Y = model.predict(x1)
pred = Y[0]

tP = 0
PrecioNow = x[0][0]
now = datetime.now()

current_time = now.strftime("%m/%d/%y %H:%M:%S")
id = now.strftime("%H:%M:%S")





if pred == 1:
    tP = x[0][0]*(1+takeProfit)
    os.system('cmd /c "color 2"')
    print("Comprar, precio:",x[0][0])
    os.system('cmd /c "color 7"')
    print("Take profit: ",tP)

    # Create order

    # SQL
    query = "INSERT INTO ordenes VALUES ("+str(current_time)+","+str(PrecioNow)+","+str(tP)+");"
    print(query)
    cur.execute(query)

    # CSV
    #with open('ordenes.csv', 'a',newline='') as myfile:
    #    writer = csv.writer(myfile, delimiter =',')
    #    writer.writerow([current_time,PrecioNow,tP])

else:
    os.system('cmd /c "color 4"')
    print("No comprar")
    os.system('cmd /c "color 7"')

# Get orders

# SQL
    

query = "SELECT * FROM ordenes;"
print(query)
cur.execute(query)
orders = cur.fetchall()
orders = pd.DataFrame(orders,columns=['id','buy','takeProfit'])


# CSV

#orders = pd.read_csv("ordenes.csv")

#--------------------------------------------


m = len(orders)
closed = []
 

for i in range(m):
    if orders.iloc[i,2] <= PrecioNow:

        # exit order

        # SQL
        query = "INSERT INTO exits VALUES ('"+str(orders.iloc[i,0])+"','"+str(orders.iloc[i,1])+"','"+str(PrecioNow)+"','"+str((PrecioNow/orders.iloc[i,1])-1)+"','"+str(1)+"');"
        print(query)
        cur.execute(query)
        query = "DELETE FROM ordenes WHERE id = '"+str(orders.iloc[i,0])+"';"
        print(query)
        cur.execute(query)

        # CSV
        #with open('exits.csv', 'a',newline='') as myfile:
        #    writer = csv.writer(myfile, delimiter =',')
        #    writer.writerow([orders.iloc[i,0],orders.iloc[i,1],PrecioNow,(PrecioNow/orders.iloc[i,1])-1,1])

        #closed.append(i)

        
    elif (now - datetime.strptime(orders.iloc[i,0],'%m/%d/%y %H:%M:%S')).total_seconds() > 60*30:
        
        # exit order

        # SQL
        query = "INSERT INTO exits VALUES ('"+str(orders.iloc[i,0])+"','"+str(orders.iloc[i,1])+"','"+str(PrecioNow)+"','"+str((PrecioNow/orders.iloc[i,1])-1)+"','"+str(0)+"');"
        print(query)
        cur.execute(query)
        query = "DELETE FROM ordenes WHERE id = '"+str(orders.iloc[i,0])+"';"
        print(query)
        cur.execute(query)

        # CSV
        #with open('exits.csv', 'a',newline='') as myfile:
        #    writer = csv.writer(myfile, delimiter =',')
        #    writer.writerow([orders.iloc[i,0],orders.iloc[i,1],PrecioNow,(PrecioNow/orders.iloc[i,1])-1,0])

        #closed.append(i)
        

# Close orders in CSV
        
#print("Ordenes")        
#print(orders.drop(closed))
#orders.drop(closed).to_csv("ordenes.csv",index=False)

#----------------------------------------------------


print("\n")