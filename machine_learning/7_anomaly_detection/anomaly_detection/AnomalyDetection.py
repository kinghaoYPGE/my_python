#! /usr/bin/env python
# encoding: utf-8
import numpy as np
import scipy.io as spio
import matplotlib.pyplot as plt


def estimateGaussian(X):
    m, n = X.shape
    mu = np.zeros((n, 1))
    sigma2 = np.zeros((n, 1))
    mu = np.mean(X, axis=0)  # 求X每一列的均值
    sigma2 = np.var(X, axis=0)  # 求每一列的方差
    return mu, sigma2


def display_2d_data(X, marker):
    plt.plot(X[:, 0], X[:, 1], marker)
    return plt


def multivariateGaussian(X, mu, sigma2):
    """
    多元高斯分布
    :param X:
    :param mu:
    :param sigma2:
    :return:
    """
    k = len(mu)
    if sigma2.shape[0] > 1:
        sigma2 = np.diag(sigma2)
    X = X - mu
    argu = (2 * np.pi) ** (-k / 2) * np.linalg.det(sigma2) ** (-0.5)
    p = argu * np.exp(-0.5 * np.sum(np.dot(X, np.linalg.inv(sigma2)) * X, axis=1))
    return p


def visualizeFit(X, mu, sigma2):
    x = np.arange(0, 36, step=0.5)
    y = np.arange(0, 36, step=0.5)
    X1, X2 = np.meshgrid(x, y)  # 计算等高线
    Z = multivariateGaussian(np.hstack((X1.reshape(-1, 1), X2.reshape(-1, 1))), mu, sigma2)
    Z = Z.reshape(X1.shape)
    plt.plot(X[:, 0], X[:, 1], 'bx')

    if np.sum(np.isinf(Z).astype(np.float)) == 0:  # 如果是无穷大，就不用画
        plt.contour(X1, X2, Z, 10. ** np.arange(-20, 0, 3), color='black', linewidth=.5)
    plt.show()


def selectThreshold(yval, pval):
    bestEpsilon = 0.
    bestF1 = 0.
    F1 = 0.
    step = (np.max(pval) - np.min(pval)) / 1000
    for epsilon in np.arange(np.min(pval), np.max(pval), step):
        cvPrecision = pval < epsilon  # 异常点
        tp = np.sum((cvPrecision == 1) & (yval == 1)).astype(float)
        fp = np.sum((cvPrecision == 1) & (yval == 0)).astype(float)
        fn = np.sum((cvPrecision == 1) & (yval == 0)).astype(float)
        precision = tp / (tp + fp)  # 查准率
        recall = tp / (tp + fn)  # 查全率
        F1 = (2 * precision * recall) / (precision + recall)
        if F1 > bestF1:
            bestF1 = F1
            bestEpsilon = epsilon
    return bestEpsilon, bestF1


def anomalyDetection():
    """
    异常检测(Anomaly Detection)
    :return:
    """
    # 加载数据
    data = spio.loadmat('data1.mat')
    X = data['X']
    plt = display_2d_data(X, 'bx')
    plt.show()

    mu, sigma2 = estimateGaussian(X)  # 得到均值和方差
    # 执行多元高斯分布函数
    p = multivariateGaussian(X, mu, sigma2)
    visualizeFit(X, mu, sigma2)

    # 选择异常临界点
    Xval = data['Xval']
    yval = data['yval']  # y=1 代表异常
    print(Xval.shape, yval.shape)
    # 计算cross validation set的概率密度值
    pval = multivariateGaussian(Xval, mu, sigma2)
    # 尝试多个异常临界点，F1score值最高
    epsilon, F1 = selectThreshold(yval, pval)
    print(u'在CV上得到的最好的epsilon是%e' % epsilon)
    print(u'对应的F1score为: %f' % F1)
    # 找到小于临界值的异常点
    outliers = np.where(p < epsilon)
    plt.plot(X[outliers, 0], X[outliers, 1],
             'o', markeredgecolor='r', markerfacecolor='w', markersize=10.)
    plt = display_2d_data(X, 'bx')
    plt.show()


if __name__ == '__main__':
    anomalyDetection()
