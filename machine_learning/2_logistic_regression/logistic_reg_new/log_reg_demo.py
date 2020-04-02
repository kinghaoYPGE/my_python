import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import fmin_bfgs


def plot_data(X, y):
    pos = np.where(y == 1)
    neg = np.where(y == 0)
    plt.plot(X[pos, 0], X[pos, 1], 'ro')
    plt.plot(X[neg, 0], X[neg, 1], 'bo')
    # plt.show()


def mapFeature(X1, X2):
    """
    example: 1+X1+X2+X1.X2+X1^2+X2^2
    :param X1:
    :param X2:
    :return:
    """
    degree = 2
    out = np.ones((X1.shape[0], 1))
    for i in range(1, degree + 1):
        for j in range(i + 1):
            temp = X1 ** (i - j) * (X2 ** j)
            out = np.hstack((out, temp.reshape(-1, 1)))
    return out


def sigmoid(z):
    """
    创建S型函数
    :param param:
    :return:
    """
    h = np.zeros((len(z), 1))
    h = 1.0 / (1.0 + np.exp(-z))
    return h


def costFunction(initial_theta, X, y, initial_lambda):
    """
    定义损失函数
    :param initial_theta:
    :param X:
    :param y:
    :param initial_lambda:
    :return:
    """
    m = len(y)
    J = 0
    h = sigmoid(np.dot(X, initial_theta))
    theta1 = initial_theta.copy()
    theta1[0] = 0
    temp = np.dot(theta1.T, theta1)
    J = (-np.dot(np.transpose(y), np.log(h)) - np.dot(np.transpose(1 - y), np.log(1 - h))
         + temp * initial_lambda / 2) / m

    return J


def gradient(initial_theta, X, y, initial_lambda):
    """
    求梯度，其实就是求偏导
    :param initial_theta:
    :param X:
    :param y:
    :param initial_lambda:
    :return:
    """
    m = len(y)
    h = sigmoid(np.dot(X, initial_theta))
    theta1 = initial_theta.copy()
    theta1[0] = 0
    grad = np.zeros((initial_theta.shape[0]))
    grad = np.dot(np.transpose(X), h - y) / m + initial_lambda / m * theta1  # 正则化的梯度
    return grad


def predict(X, theta):
    """
    预测
    :param X:
    :param result:
    :return:
    """
    m = X.shape[0]
    p = np.zeros((m, 1))
    p = sigmoid(np.dot(X, theta))
    for i in range(m):
        if p[i] >= 0.5:
            p[i] = 1
        else:
            p[i] = 0
    return p


def plotDecisionBoundary(theta, X, y):
    """
    画出决策边界
    :param result:
    :param X:
    :param y:
    :return:
    """
    plot_data(X, y)
    u = np.linspace(-1, 1.5, 50)  # 根据具体的数据，这里需要调整
    v = np.linspace(-1, 1.5, 50)

    z = np.zeros((len(u), len(v)))
    for i in range(len(u)):
        for j in range(len(v)):
            z[i, j] = np.dot(mapFeature(u[i].reshape(1, -1), v[j].reshape(1, -1)), theta)  # 计算对应的值，需要map

    z = np.transpose(z)
    plt.contour(u, v, z, [0, 0.01])  # 画等高线，范围在[0,0.01]，即近似为决策边界
    # plt.legend()
    plt.show()


def LogisticRegression():
    data = np.loadtxt('data1.txt', delimiter=',', dtype=np.float)  # (118, 3)
    X = data[:, :-1]
    y = data[:, -1]
    plot_data(X, y)  # 画出两种特征的分布图
    X = mapFeature(X[:, 0], X[:, 1])  # 通过观察，发现这里的决策边界不是线性的，是一个椭圆，所以需要映射为多项式
    initial_theta = np.zeros((X.shape[1], 1))  # 初始化theta
    initial_lambda = 0.1  # 初始化正则化系数, 一般取值0.01, 0.03, 0.1, 0.3...
    J = costFunction(initial_theta, X, y, initial_lambda)
    print(J)
    # 使用scipy的牛顿法实现梯度下降
    result = fmin_bfgs(costFunction, initial_theta, fprime=gradient, args=(X, y, initial_lambda))
    print(result)
    p = predict(X, result)
    print('预测准确率为%f%%' % np.mean(np.float64(p == y) * 100))
    X_origin = data[:, :-1]
    plotDecisionBoundary(result, X_origin, y)  # 画出决策边界


def testLogisticRegression():
    LogisticRegression()


if __name__ == '__main__':
    testLogisticRegression()
