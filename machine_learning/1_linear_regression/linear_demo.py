import numpy as np
from numpy.linalg import inv
from numpy import dot, array
from numpy import mat

"""
线性回归(linear regression)    
    1. 实现最小二乘法
    Y = 2X
    theta = (X'X)^-1X'Y
    
    2. 实现梯度下降
    theta = theta - alpha*(theta*X -Y)*X
    init: alpha = 0.1, theta = 3 

"""
X = mat([1, 2, 3, 4, 5, 6]).reshape(6, 1)  # data set
Y = mat([4, 5, 7, 5, 9, 12]).reshape(6, 1)
# hypothesis Y = theta * X

# theta = inv(X.T * X)*X.T*Y #最小二乘法
theta = 1.
alpha = 0.01
# print(alpha * (theta * X - Y) * X.T)
# print(np.sum(alpha * (theta * X - Y) * X.T))

for i in range(100):
    theta = theta - np.sum(alpha * (theta * X - Y) * X.T) / 6.
    # theta = theta + np.sum(alpha * (Y - dot(X, theta)) * X.reshape(1, 6)) / 6.
print(theta)
