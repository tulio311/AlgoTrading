import joblib
import pandas as pd
import os
import csv
from datetime import datetime

os.system('cmd /c "node Prices.js"')

model = joblib.load("modelo.joblib")

takeProfit = .002


x1 = pd.read_csv("PreciosNow.csv")


x = [[x1.iloc[0,0],x1.iloc[0,1],x1.iloc[0,2],x1.iloc[0,3]]]

Y = model.predict(x1)

tP = 0
PrecioNow = x[0][0]
now = datetime.now()

current_time = now.strftime("%m/%d/%y %H:%M:%S")
id = now.strftime("%H:%M:%S")


if Y[0] == 1:
    tP = x[0][0]*(1+takeProfit)
    os.system('cmd /c "color 2"')
    print("Comprar, precio:",x[0][0])
    os.system('cmd /c "color 7"')
    print("Take profit: ",tP)

    with open('ordenes.csv', 'a',newline='') as myfile:
        writer = csv.writer(myfile, delimiter =',')
        writer.writerow([current_time,PrecioNow,tP])

else:
    os.system('cmd /c "color 4"')
    print("No comprar")
    os.system('cmd /c "color 7"')

# Cerrar órdenes
    
orders = pd.read_csv("ordenes.csv")
m = len(orders)
closed = []
 
for i in range(m):
    if orders.iloc[i,2] <= PrecioNow:
        with open('exits.csv', 'a',newline='') as myfile:
            writer = csv.writer(myfile, delimiter =',')
            writer.writerow([orders.iloc[i,0],orders.iloc[i,1],PrecioNow,(PrecioNow/orders.iloc[i,1])-1,1])

        closed.append(i)
        
    elif (now - datetime.strptime(orders.iloc[i,0],'%m/%d/%y %H:%M:%S')).total_seconds() > 60*30:
        with open('exits.csv', 'a',newline='') as myfile:
            writer = csv.writer(myfile, delimiter =',')
            writer.writerow([orders.iloc[i,0],orders.iloc[i,1],PrecioNow,(PrecioNow/orders.iloc[i,1])-1,0])
        
        closed.append(i)
        
print("Ordenes")        
print(orders.drop(closed))
orders.drop(closed).to_csv("ordenes.csv",index=False)

print("\n")