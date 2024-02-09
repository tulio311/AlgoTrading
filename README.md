# Algorithmic Trading

This is an algorithmic trading system for cryptocurrency. The step of placing and closing orders automatically is missing because the time frame for which this system was designed is very small and . Despite of this, it has all the other parts of the system already automatized. It gets the necessary information to decide if it is the correct moment to trade and process
it with the designated model. Then it tells the user by console if it is the moment or if it is not.

The model is based on a training set with the prices of 4 cryptos (Btc,Eth,Bch,Xrp) and a objective value (0 or 1). The objective is 1 if the price of Btc rose more than x% in
the next half hour from the registering of the 4 prices and is 0 if not (x being a percentage parameter than can be modified depending of observations). This data set for training may not be optimal but the purpose of this experiment is also to measure the extent in which the prices of some cryptos can influence the price of Bitcoin.

The model can be thought as 2 separated pipelines. The modeling pipeline or protocol and the execution pipeline. The former consists of gathering data, organizing it, labeling it with the objective variable and using it to compare models with the purpose of defining the best one (Or at least the one which seems like the best with the gathered data). The execution pipeline consists of the chain of processes needed to find the correct moment to buy using the designated model trained with the gathered data in the modeling protocol. 

# bucle.py

This file is the starting point of the algorithm in the execution pipeline. It has the main loop, which executes every 10 seconds approximately. It runs the runModel.py file.

# runModel.py

At first, this code runs the Prices.js code in Node.js, which asks the prices of  


