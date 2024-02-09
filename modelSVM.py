import pandas as pd
import joblib
from sklearn.svm import SVC

cota = "002"

X = pd.read_csv("4criptoLabeled"+cota+".csv")

data = X.iloc[:,:4]
Labels = X.iloc[:,4]

COpt = 1
kernelOpt = "linear"


model = SVC(C= COpt,kernel= kernelOpt)
model.fit(data,Labels)



joblib.dump(model,"modelo.joblib")