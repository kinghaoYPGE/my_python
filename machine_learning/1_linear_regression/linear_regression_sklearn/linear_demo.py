#! /usr/bin/env python
# encoding: utf-8
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# Step 1: Pre-Process the data
dataSet = pd.read_csv('studentscores.csv')
X = dataSet.iloc[:, : 1].values
Y = dataSet.iloc[:, 1].values

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=1 / 4, random_state=0)

# Step 2: Fitting model to the training set
regressor = LinearRegression().fit(X_train, Y_train)

# Step 3: Predicting the result
Y_pred = regressor.predict(X_test)
print(Y_pred, Y_test)

# Step 4: Visualization
# Visualising the Training results
plt.scatter(X_train, Y_train, color='red')
plt.plot(X_train, regressor.predict(X_train), color='blue')

# Visualizing the test results
plt.scatter(X_test, Y_test, color='red')
plt.plot(X_test, regressor.predict(X_test), color='blue')

plt.show()

