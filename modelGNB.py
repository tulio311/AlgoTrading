from sklearn.naive_bayes import GaussianNB
import numpy as np
import pandas as pd
import joblib

cota = "002"

X = pd.read_csv("4criptoLabeled" + cota + ".csv")

data = X.iloc[:,:4]
Labels = X.iloc[:,4]


print(data)
print(Labels)

model = GaussianNB()

model.fit(data,Labels)


joblib.dump(model,"modelo.joblib")