#! /usr/bin/env python
# encoding: utf-8
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

dataSet = pd.read_csv('50_Startups.csv')
m = len(dataSet)
X = dataSet.iloc[:, :-1].values  # m * 4
Y = dataSet.iloc[:, -1].values  # 1 * m

# Encoding Categorical data
laberEncoder = LabelEncoder()
X[:, 3] = laberEncoder.fit_transform(X[:, 3])
oneHotEncoder = OneHotEncoder(categorical_features=[3])
X = oneHotEncoder.fit_transform(X).toarray()

# Avoiding Dummy Variable Trap
X = X[:, 1:]

# Splitting the dataset into the Training set and Test set
X_TRAIN, X_TEST, Y_TRAIN, Y_TEST = train_test_split(X, Y, test_size=0.2, random_state=0)

# Step2 : Fitting Multiple Linear Regression to the Training set
regressor = LinearRegression()
regressor.fit(X_TRAIN, Y_TRAIN)

# Step 3: Predicting the Test set results
y_pred = regressor.predict(X_TEST)
print('y test: {0} y pred: {1}'.format(Y_TEST, y_pred))
