from sklearn.naive_bayes import GaussianNB
import numpy as np
import pandas as pd
import joblib
from xgboost import XGBClassifier
from sklearn.model_selection import KFold
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

fullData = X.iloc[:,:4]
fullLabels = X.iloc[:,4]

folds = 4

kFolds = KFold(n_splits=folds,  random_state=100, shuffle=True)

trainX,testX, trainY,testY = train_test_split(fullData,fullLabels,test_size=.3)

data = trainX
Labels = trainY

valid = X.iloc[:,:4]
validLabels = X.iloc[:,4]


n = len(validLabels)

max = 0
avg = 0

# Naive Bayes Gaussiano

for i, (train_index, test_index) in enumerate(kFolds.split(fullData)):

    print((train_index, test_index))

    modelGNB = GaussianNB()

    modelGNB.fit(fullData.iloc[train_index],fullLabels[train_index])

    Y = modelGNB.predict(fullData.iloc[test_index]) 

    suma = 0

    print(Y)
    valid = fullLabels.iloc[test_index].reset_index().iloc[:,1]
    print(valid)

    for j in range(len(Y)):
        #print(fullLabels.iloc[test_index].iloc[j])
        if Y[j] == valid.iloc[j]:
            suma = suma + 1/len(Y)

    avg = avg + suma/folds
    print(suma)
    
max = avg
print("Naive Bayes, Accuracy: ",max)



# XGBoost

arbOpt = 0
etaOpt = 0
profOpt = 0
gammaOpt = 0


arboles = [4,6,8,9,10]
etas = [0.05,0.08,1,1.2,1.5]
profs = [6,7,8,9,10]
gammas = [0,0.1,0.2]

ind = 0

for arb in arboles:
    for eta in etas:
        for prof in profs:
            for gamma in gammas:
                
                avg = 0
                print("arboles: ",arb,"eta: ",eta,"profundidad: ",prof,"gamma: ",gamma)

                for i, (train_index, test_index) in enumerate(kFolds.split(fullData)):

                    model = XGBClassifier(n_estimators=arb,objective='binary:logistic',eta=eta,
                        max_depth=prof,gamma = gamma,min_child_weight = 1,scale_pos_weight = 1)
                    model.fit(fullData.iloc[train_index],fullLabels[train_index])
                
                    Y = model.predict(fullData.iloc[test_index])
                    suma = 0
                    valid = fullLabels.iloc[test_index].reset_index().iloc[:,1]

                    for j in range(len(Y)):
                        if Y[j] == valid.iloc[j]:
                            suma = suma + 1/len(Y)

                    print(suma)
                    avg = avg + suma/folds


                if avg > max:
                    ind = 1
                    arbOpt = arb
                    etaOpt = eta
                    profOpt = prof
                    gammaOpt = gamma
                    max = avg
                print("Accuracy ",avg)





# Random Forest

arbolesF = [60,70,80,90,100]
crits = ["gini", "entropy", "log_loss"]

arbFOpt = 0
critOpt = ""

for arb in arbolesF:
    for crit in crits:
        avg = 0
        print("arbolesF: ",arb,"crit: ",crit)

        for i, (train_index, test_index) in enumerate(kFolds.split(fullData)):
            model = RandomForestClassifier(n_estimators=arb,criterion=crit)
            model.fit(fullData.iloc[train_index],fullLabels[train_index])
                
            Y = model.predict(fullData.iloc[test_index])
            suma = 0
            valid = fullLabels.iloc[test_index].reset_index().iloc[:,1]

            for j in range(len(Y)):
                if Y[j] == valid.iloc[j]:
                    suma = suma + 1/len(Y)
            print(suma)
            avg = avg + suma/folds

        if avg > max:
            ind = 2 
            max = avg
            arbFOpt = arb
            critOpt = crit
        print("Accuracy: ",avg)


# SVC
        

Cs = [0.8,1.2]
kernels = ["linear", "poly", "rbf", "sigmoid"]


COpt = 0
kernelOpt = 0

for C in Cs:
    for kernel in kernels:

        avg = 0
        print("C: ",C,"kernel: ",kernel)

        for i, (train_index, test_index) in enumerate(kFolds.split(fullData)):
            model = SVC(C= C,kernel= kernel)
            model.fit(fullData.iloc[train_index],fullLabels[train_index])
                
            Y = model.predict(fullData.iloc[test_index])
            suma = 0
            valid = fullLabels.iloc[test_index].reset_index().iloc[:,1]

            for j in range(len(Y)):
                if Y[j] == valid.iloc[j]:
                    suma = suma + 1/len(Y)
            print(suma)
            avg = avg + suma/folds

        if avg > max:
            ind = 3 
            max = avg
            COpt = C
            kernelOpt = kernel
           
        print("Accuracy: ",avg)
      







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

