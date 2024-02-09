from xgboost import XGBClassifier
import pandas as pd
import joblib

cota = "002"

X = pd.read_csv("4criptoLabeled"+cota+".csv")

data = X.iloc[:,:4]
Labels = X.iloc[:,4]

arb = 6
eta = 1.2
prof = 6
gamma = 0

model = XGBClassifier(n_estimators=arb,objective='binary:logistic',eta=eta,
                      max_depth=prof,gamma = gamma,min_child_weight = 1,scale_pos_weight = 1)
model.fit(data,Labels)

joblib.dump(model,"modelo.joblib")