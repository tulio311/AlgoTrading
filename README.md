# Algorithmic Trading

This is an algorithmic trading system for cryptocurrency. The step of placing and closing orders automatically is missing because the time frame for which this system was designed is very small and seeing the prices increments data thrown by the market, the spreads offered by the crypto exchanges don't let this system be profitable. Despite of this, it has all the other parts of the system already automatized, and its ideas can be applied in longer time frames if the data for that longer time frames is available. 

The model is based on a training dataset with the prices of 4 cryptos (Btc,Eth,Bch,Xrp) and a objective value (0 or 1). The objective is 1 if the price of Btc rose more than x% in
the next half hour from the registering of the 4 prices and is 0 if not (x being a percentage parameter than can be modified depending of observations). This data set for training may not be optimal but the purpose of this experiment is also to measure the extent in which the prices of some cryptos can influence the price of Bitcoin (The algorithm is now focused in Btc but it can focus in any of the other 3 cryptos in the model).

The model can be thought as 2 separated pipelines. The modeling pipeline or protocol and the execution pipeline. The former consists of gathering data, organizing it, labeling it with the objective variable and using it to compare models with the purpose of finding the best one (or at least the one which seems like the best with the gathered data). The execution pipeline consists of the chain of processes needed to find the correct moment to buy using the designated model trained with the gathered data in the modeling protocol. 

The processes related with training datasets, buy and sell orders and prices actualization exist in 2 variants. SQL database (using SQLite with the database `Algo.db`) and CSV files. The active uncommented version is the SQL version, the other one is commented and marked in the scripts where this option is available. 

## Modeling protocol

The system tries to solve a classification problem. We want to predict, based on the prices of this 4 cryptos in a certain time, if the price of Btc will go up certain percentage in the next half an hour. In order to do this we have to gather series data and define the percentage x% that we have to target to. We have to rely on the real market data to fix a reachable objective for this x in this period of time.

### Crypto.js

This script is designed to get the prices of the 4 crytos involved from Bitso's API every 5 minutes along a given time span and then run the cleaning and modeling scripts (The execution of `Crypto.js` makes all the ETL process followed by the modeling process made with this new information). The code as it is right now does the prices extraction for 3 hours.

Each time the prices are asked, the script writes them in the file `criptos.csv`. The job of this script is to gather sequential prices data in order to train the model. The optimal thing is to run this script in different days in order to obtain data from different financial environments. The divisions between different continued periods of prices extraction every 5 minutes are marked with a line of dots in `criptos.csv`. This is important in the modeling phase because we'll have to throw out the 6 last records of each period because we don't have a way to know if the price of Btc reached the objective in the next 30 minutes. Despite of this, the prices of Btc in this last 6 rows are important for knowing if the prior records achieved the objective.

After gathering the information in the selected time span, the script calls out `process.py`, which will clean the new information and insert it in the storage system. Then, the script calls out `allModels.py`, this is the script that takes the modeling decision with the new information and trains the new model. 

### process.py

This is the transforming script of the raw data from the time span selected in `Crypto.js`. It creates a new column in this data with the maximum price of Btc achieved in the next 30 minutes after each row was registered (just taking into consideration the prices recorded each 5 minutes), and after this, we can throw out the last 6 records. Then, the script calculates the percentage gained or lost by Btc to this maximum. This data is the one which we have to rely on in order to set the adecuate x%. Based on the data found so far, I have seen that x = 0.001 and x = 0.002 are reasonable takes. The percentage of instances in which the coin achieves a percentage between this ones is more or less 30% in most cases.

The script then creates a label for each record (being 0 or 1) indicating if the record achieved or not the goal of the designated percentage growth. The 4 prices columns joined with this labels conform the training information related to this new information. This information is now pushed into the `training` table in the database.  

In the CSV storage version, the files `4criptoLabeled001.csv` and `4criptoLabeled002.csv` have the records joined with the objective (0 or 1) that label if a record achieved the respective objective (0.001% or 0.002%) in the next half and hour. These two are the training datasets for this storage version.

### allModels.py

The job of this script is to find the best model. It tests different parametrizations for Random Forest, XGBoost, SVM and Gaussian Naive-Bayes (not different parametrizations for this one). The script tests all the models in all the parametrizations trained with 70% of the dataset (This is the dataset obtained from the `training` table). The validation is made in the whole dataset (not just in the 30% left because I don't have enough data so far to rely on that). 

When the script finds the most accurate model, it launches the adequate python script which will train and save the model.

### Training

Depending on the model chosen in the last step, the model is trained with the full dataset in one of the scripts `modelGNB.py` (Gaussian Naive-Bayes), `modelRF.py` (Random Forest), `modelXGB.py` (XGBoost) and `modelSVM.py` (SVM). The adecuate script is automatically launched by `allModels.py` and the communication of the chosen parameters between this script and the training one is the CSV file `parametros.csv`.

The trained model is saved in `modelo.joblib` and then it can be used in the execution pipeline.



## Execution pipeline

### bucle.py

This file is the starting point of the algorithm in the execution pipeline. It has the main loop, which executes every 10 seconds approximately. It just runs the `runModel.py` file every loop.

### runModel.py

At first, this code runs the `Prices.js` code in `Node.js`, which asks the prices of the cryptos in that moment and writes them in the table `PreciosNow` while deleting the past prices. This is for communicating with this python script. Then, the script gets this data and run the pretrained model saved as `modelo.joblib`. The model decides if it is time to buy or not with the given prices. The script then anounces if this is the case or not and if so, it writes the open order in the table `ordenes`, indicating the buy time and price, and the take profit price based on the profit percentage designated in the modeling protocol. 

At the end, this sript checks if it is the moment to close some of the open orders in the `ordenes` table. The script closes an order if it has achieved the take profit mark or if it has been passed 30 minutes from the creation of the order. This is because the model have been designed to try to predict if the price of Bitcoin will rise determined percentage in the next 30 minutes. For each order that the system decides to close, it is deleted from `ordenes` and added to the table `exits`, indicating if the order was closed because of take profit or time. This is for measuring the success rate of the model deciding when the price will go up in the next 30 minutes.







