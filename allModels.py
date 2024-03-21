from sklearn.naive_bayes import GaussianNB
import numpy as np
import pandas as pd
import joblib
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
import os
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

rawData = X.iloc[:,:4]
rawLabels = X.iloc[:,4]

trainX,testX, trainY,testY = train_test_split(rawData,rawLabels,test_size=.3)

data = trainX
Labels = trainY

valid = X.iloc[:,:4]
validLabels = X.iloc[:,4]


n = len(validLabels)

# Naive Bayes Gaussiano

modelGNB = GaussianNB()

modelGNB.fit(data,Labels)

Y = modelGNB.predict(valid)

suma = 0

for i in range(n):
    if Y[i] == validLabels[i]:
        suma = suma + 1/n
    
max = suma
print("Naive Bayes, Correcto: ",max)



# XGBoost

arbOpt = 0
etaOpt = 0
profOpt = 0
gammaOpt = 0
max = 0

arboles = [4,6,8,9,10]
etas = [0.05,0.08,1,1.2,1.5]
profs = [6,7,8,9,10]
gammas = [0,0.1,0.2]

ind = 0
for arb in arboles:
    for eta in etas:
        for prof in profs:
            for gamma in gammas:
                print("arboles: ",arb,"eta: ",eta,"profundidad: ",prof,"gamma: ",gamma)
                model = XGBClassifier(n_estimators=arb,objective='binary:logistic',eta=eta,
                      max_depth=prof,gamma = gamma,min_child_weight = 1,scale_pos_weight = 1)
                model.fit(data,Labels)
            
                Y = model.predict(valid)
                suma = 0
                for i in range(n):
                    if Y[i] == validLabels[i]:
                        suma = suma + 1/n
                if suma > max:
                    ind = 1
                    arbOpt = arb
                    etaOpt = eta
                    profOpt = prof
                    gammaOpt = gamma
                    max = suma
                print("Correcto: ",suma)

# Random Forest

arbolesF = [60,70,80,90,100]
crits = ["gini", "entropy", "log_loss"]

arbFOpt = 0
critOpt = ""

for arb in arbolesF:
    for crit in crits:
        print("arbolesF: ",arb,"crit: ",crit)
        model = RandomForestClassifier(n_estimators=arb,criterion=crit)
        model.fit(data,Labels)
            
        Y = model.predict(valid)
        suma = 0
        for i in range(n):
            if Y[i] == validLabels[i]:
                suma = suma + 1/n
        if suma > max:
            ind = 2 
            max = suma
            arbFOpt = arb
            critOpt = crit
        print("Correcto: ",suma)


# SVC
        

Cs = [0.8,1,1.2]
kernels = ["linear", "poly", "rbf", "sigmoid"]


COpt = 0
kernelOpt = 0
gammaSVCOpt = 0

for C in Cs:
    for kernel in kernels:
        print("C: ",C,"kernel: ",kernel)
        model = SVC(C= C,kernel= kernel)
        model.fit(data,Labels)
            
        Y = model.predict(valid)
        suma = 0
        for i in range(n):
            if Y[i] == validLabels[i]:
                suma = suma + 1/n
        if suma > max:
            ind = 3 
            max = suma
            COpt = C
            kernelOpt = kernel
           
        print("Correcto: ",suma)
      







# Mejor modelo

if ind == 1:
    print("xgboost")
    print("arbolesOpt: ",arbOpt,"etaOpt: ",etaOpt,"profOpt: ",profOpt,"gammaOpt: ",gammaOpt)
    print("Accuracy: ",max)
    par = {'arbOpt':[arbOpt],'etaOpt':[etaOpt],'profOpt':[profOpt],'gammaOpt':[gammaOpt]}
    pd.DataFrame(par).to_csv("parametros.csv",index=False)
    os.system("cmd /c python modelXGB.py "+str(arbOpt)+" "+str(etaOpt)+" "+str(profOpt)+" "+str(gammaOpt))

elif ind == 2:
    print("Random Forest")
    print("arbolesFOpt: ",arbFOpt,"critOpt: ",critOpt)
    print("Accuracy: ",max)
    par = {"arbolesFOpt":[arbFOpt],"critOpt":[critOpt]}
    pd.DataFrame(par).to_csv("parametros.csv",index=False)
    os.system(f"cmd /c python modelRF.py {arbFOpt} {critOpt}")

elif ind == 3:
    print("SVC")
    print("C: ",COpt,"kernel: ",kernelOpt)
    print("Accuracy: ",max)
    par = {"C":[COpt],"kernel":[kernelOpt]}
    pd.DataFrame(par).to_csv("parametros.csv",index=False)
    os.system(f"cmd /c python modelSVC.py {COpt} {kernelOpt}")

else:    
    print("Naive Bayes")
    print("Accuracy: ",max)
    os.system("cmd /c python modelGNB.py")

