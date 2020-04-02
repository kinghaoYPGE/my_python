#! /usr/bin/env python
# encoding: utf-8
import numpy as np
import pandas as pd
from numpy.linalg import inv
from numpy import dot

"""
使用线性回归对房屋价格进行预测，数据来自于爬虫
这里， 我们分别使用最小二乘法和梯度下降来实现
"""

dataSet = pd.read_csv('houses.csv', delimiter='|', usecols=[1, 2, 4])

temp = dataSet.iloc[:, [1, 2]]
temp['X0'] = 1
temp['X1'] = temp['size']
temp['X2'] = [float(i[0]) for i in temp['type']]
temp['X3'] = [float(i[2]) for i in temp['type']]

X = temp.iloc[:, [2, 3, 4, 5]]

Y = dataSet.iloc[:, 0].values.reshape(60, 1)

# 最小二乘法
# theta = (X'X)^-1X'Y
theta = dot(dot(inv(dot(X.T, X)), X.T), Y)
print(theta)

# 梯度下降
alpha = 0.1
theta = np.array([1., 1., 1., 1.]).reshape(4, 1)
X0 = X.iloc[:, 0].values.reshape(60, 1)
X1 = X.iloc[:, 1].values.reshape(60, 1)
X2 = X.iloc[:, 2].values.reshape(60, 1)
X3 = X.iloc[:, 3].values.reshape(60, 1)
temp_theta = theta

for i in range(10000):
    temp_theta[0] = temp_theta[0] + alpha*np.sum((Y-dot(X, theta))*X0)/60
    temp_theta[1] = temp_theta[1] + alpha*np.sum((Y-dot(X, theta))*X1)/60
    temp_theta[2] = temp_theta[2] + alpha*np.sum((Y-dot(X, theta))*X2)/60
    temp_theta[3] = temp_theta[3] + alpha*np.sum((Y-dot(X, theta))*X3)/60
    theta = temp_theta

print(theta)



