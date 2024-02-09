import numpy as np
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier

cota = "002"

X = pd.read_csv("4criptoLabeled"+cota+".csv")

data = X.iloc[:,:4]
Labels = X.iloc[:,4]

arb = 60
crit = "log_loss"


model = RandomForestClassifier(n_estimators=arb,criterion=crit)
model.fit(data,Labels)



joblib.dump(model,"modelo.joblib")