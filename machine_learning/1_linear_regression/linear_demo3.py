import numpy as np
from numpy.linalg import inv
import pandas as pd
from numpy import dot

df = pd.read_csv('training.csv', delimiter='|', usecols=[1, 2, 3, 4, 5])

"""
使用最小二乘法求出theta
公式:
theta = (X.T*X)^-1*X.T*Y
"""
df = df.dropna()
means = df.mean()
maxs = df.max()
m = len(df)

# 由于X的值范围相差较大，要进行特征缩放
df['price'] = df['price'].apply(lambda x: x / maxs['price'])
df['size'] = df['size'].apply(lambda x: x / maxs['size'])
df['type'] = df['type'].apply(lambda x: x / maxs['type'])
df['floor'] = df['floor'].apply(lambda x: x / maxs['floor'])
df['year'] = df['year'].apply(lambda x: x / maxs['year'])
# df['offset'] = 1

X = df.iloc[:, [1, 2, 3, 4]]
Y = df['price'].values.reshape(m, 1)

theta = dot(dot(inv(dot(X.T, X)), X.T), Y)
print(theta)

"""
使用梯度下降求出theta
公式:
theta = theta - alpha*(1/m)*sum(theta*X-Y)*X
"""
alpha = 0.1
theta = np.array([1., 1., 1., 1.]).reshape(4, 1)
temp = theta
X0 = X.iloc[:, 0].values.reshape(m, 1)
X1 = X.iloc[:, 1].values.reshape(m, 1)
X2 = X.iloc[:, 2].values.reshape(m, 1)
X3 = X.iloc[:, 3].values.reshape(m, 1)
# X4 = X.iloc[:, 4].values.reshape(m, 1)

for i in range(20000):
    temp[0] = theta[0] + alpha * np.sum((Y - dot(X, theta)) * X0) / m
    temp[1] = theta[1] + alpha * np.sum((Y - dot(X, theta)) * X1) / m
    temp[2] = theta[2] + alpha * np.sum((Y - dot(X, theta)) * X2) / m
    temp[3] = theta[3] + alpha * np.sum((Y - dot(X, theta)) * X3) / m
    # temp[4] = theta[4] + alpha * np.sum((Y - dot(X, theta)) * X4) / m

    theta = temp

print(theta)
