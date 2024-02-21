# Algorithmic Trading

This is an algorithmic trading system for cryptocurrency. The step of placing and closing orders automatically is missing because the time frame for which this system was designed is very short. Due to the rapid price fluctuations observed in the market and the narrow spreads offered by crypto exchanges, this system is not profitable. However, all other parts of the system are already automated, and its concepts can be applied to longer time frames if the necessary data is available.

The model is based on a training dataset containing the prices of four cryptocurrencies (BTC, ETH, BCH, XRP) and an objective value (0 or 1). The objective value is 1 if the price of BTC rises by more than x% in the next half hour from the recording of the four prices, and 0 otherwise (where x is a percentage parameter that can be modified based on observations). While the training dataset may not be optimal, the purpose of this experiment is to measure the extent to which the prices of certain cryptocurrencies can influence the price of Bitcoin. Currently, the algorithm is focused on BTC, but it can also be adapted to focus on any of the other three cryptocurrencies in the model.

The model can be conceptualized as two separate pipelines: the modeling pipeline (or protocol) and the execution pipeline.

The modeling pipeline involves gathering data, organizing it, labeling it with the objective variable, and utilizing it to compare models with the aim of finding the best one (or, at least, the one that appears to be the best given the gathered data).

On the other hand, the execution pipeline comprises the sequence of processes required to identify the optimal moment to buy using the designated model trained with the gathered data in the modeling protocol.

The processes related to training datasets, buy and sell orders, and price updates exist in two variants: SQL database (utilizing SQLite with the database `Algo.db`) and CSV files.

The active, uncommented version is the SQL version, while the other option is commented and marked in the scripts where this alternative is available.

## Modeling protocol

The system aims to solve a classification problem. Our goal is to predict, based on the prices of these four cryptocurrencies at a certain time, whether the price of BTC will increase by a certain percentage in the next half hour. To accomplish this, we need to collect time-series data and define the percentage threshold, denoted as 'x%', that we aim to target. To determine this threshold, we rely on real market data to establish a feasible objective for 'x' within this time period.

### Crypto.js

This script is designed to fetch the prices of the four cryptocurrencies involved from Bitso's API every 5 minutes over a specified time span. Subsequently, it executes the cleaning and modeling scripts. (The execution of `Crypto.js` encompasses the entire ETL process followed by the modeling process, incorporating the newly acquired information). As it stands, the code retrieves price data for a duration of 3 hours.

Each time the prices are asked, the script writes them in the file `criptos.csv`. The job of this script is to gather sequential prices data in order to train the model. The optimal thing is to run this script in different days in order to obtain data from different financial environments. The divisions between different continued periods of prices extraction every 5 minutes are marked with a line of dots in `criptos.csv`. This is important in the modeling phase because we'll have to throw out the 6 last records of each period because we don't have a way to know if the price of Btc reached the objective in the next 30 minutes. Despite of this, the prices of Btc in this last 6 rows are important for knowing if the prior records achieved the objective.

After gathering the information within the selected time span, the script invokes `process.py`, which cleans the new information and inserts it into the storage system. Subsequently, the script invokes `allModels.py`. This script is responsible for making modeling decisions based on the new information and training the new model.

### process.py

This is the transformation script for the raw data extracted during the selected time span in `Crypto.js`. It adds a new column to this data containing the maximum price of BTC achieved in the next 30 minutes after each row was recorded (considering only the prices recorded every 5 minutes). Subsequently, we can discard the last 6 records. The script then calculates the percentage gained or lost by BTC relative to this maximum price. This data serves as the basis for determining the appropriate threshold, denoted as 'x%'. Based on the data collected so far, I have observed that values of x = 0.001 and x = 0.002 are reasonable. The percentage of instances in which the coin achieves a percentage between these values is approximately 30% in most cases.

The script then assigns a label to each record, denoted as 0 or 1, indicating whether the record achieved the designated percentage growth goal. The four price columns, along with these labels, comprise the training data associated with this new information. Subsequently, this information is inserted into the `training` table in the database. 

In the CSV storage version, the files `4criptoLabeled001.csv` and `4criptoLabeled002.csv` contain records combined with the corresponding objective labels (0 or 1), indicating whether a record achieved the respective objective (0.001% or 0.002%) in the next half hour. These two files serve as the training datasets for this storage version.

### allModels.py

The purpose of this script is to identify the best model. It tests various parameterizations for Random Forest, XGBoost, SVM, and Gaussian Naive-Bayes (although no different parameterizations are tested for the latter). The script evaluates all models with all parameterizations trained on 70% of the dataset (this dataset is obtained from the `training` table). Validation is performed on the entire dataset, rather than just the remaining 30%, due to insufficient data to rely solely on the latter.

When the script identifies the most accurate model, it executes the corresponding Python script, which will train and save the model.

### Training

Depending on the model chosen in the last step, the model is trained with the full dataset using one of the scripts: `modelGNB.py` (Gaussian Naive-Bayes), `modelRF.py` (Random Forest), `modelXGB.py` (XGBoost), or `modelSVM.py` (SVM). The appropriate script is automatically executed by `allModels.py`, and the communication of the chosen parameters between this script and the training one is facilitated through the CSV file `parametros.csv`.

The trained model is saved as `modelo.joblib` and can subsequently be utilized in the execution pipeline.



## Execution pipeline

### bucle.py

This file serves as the starting point of the algorithm in the execution pipeline. It contains the main loop, which executes approximately every 10 seconds. The main task of this loop is to run the `runModel.py` file in each iteration.

### runModel.py

At first, this code runs the `Prices.js` code in `Node.js`, which asks the prices of the cryptos in that moment and writes them in the table `PreciosNow` while deleting the past prices. This interaction facilitates communication with this python script. Then, the script gets this data and run the pretrained model saved as `modelo.joblib`. The model decides if it is time to buy or not with the given prices. The script then anounces if this is the case or not and if so, it writes the open order in the table `ordenes`. It indicates the buy time and price, and the take profit price based on the profit percentage designated in the modeling protocol. 

At the end, this script checks whether it's time to close any of the open orders in the `ordenes` table. An order is closed if it has reached the take profit mark or if 30 minutes have passed since the order was created. This is because the model has been designed to predict whether the price of Bitcoin will rise by a certain percentage in the next 30 minutes.

For each order that the system decides to close, it is removed from the `ordenes` table and added to the `exits` table, indicating whether the order was closed due to take profit or elapsed time. This indicator is implemented to measure the success rate of the model in predicting price increases within the next 30 minutes.







