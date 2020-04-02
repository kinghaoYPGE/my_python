# ! /usr/bin/env python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# 加载数据集文件(txt, csv, excel, database...)
def load_txt_csv(filename, split):
    return np.loadtxt(filename, delimiter=split)


# 加载npy文件
def load_npy(filename):
    return np.load(filename)


# 计算损失函数
def computerCost(X, y, theta):
    m = len(y)
    j = (np.transpose(X * theta - y)) * (X * theta - y) / 2 * m

    return j


# 梯度下降
def gradientDescent(X, y, theta, alpha, num_iters):
    m = len(y)
    n = len(theta)
    # 初始化theta并放到temp中
    # 这样写的好处会记录下theta的变化
    temp = np.matrix(np.zeros((n, num_iters)))
    J_history = np.zeros((num_iters, 1))

    for i in range(num_iters):
        h = np.dot(X, theta)
        temp[:, i] = theta - (alpha / m) * (np.dot(np.transpose(X), h - y))
        theta = temp[:, i]
        J_history[i] = computerCost(X, y, theta)

    return theta, J_history


# 特征缩放
def featureScaling(X):
    X_Scaler = np.array(X)
    # 得到X的列数
    n = X.shape[1]
    mu = np.zeros((1, n))  # 平均数
    sigma = np.zeros((1, n))  # 标准差
    mu = np.mean(X_Scaler, 0)  # 各列平均数
    sigma = np.std(X_Scaler, 0)  # 各列标准差

    for i in range(n):
        X_Scaler[:, i] = (X_Scaler[:, i] - mu[i]) / sigma[i]

    return X_Scaler, mu, sigma


# 画二维图
def plot2D(X):
    plt.scatter(X[:, 0], X[:, 1], color='red')
    plt.show()


# 画每次迭代代价的变化图
def plotJ(J_history, num_iters):
    X = np.arange(1, num_iters + 1)  # 创建一个间隔为1的等差数组
    plt.plot(X, J_history, color='blue')
    plt.xlabel('number of iterate')
    plt.ylabel(r'J(theta)')
    plt.title('change of cost J with iterator')
    plt.show()


# 画出线性拟合情况
# def plotHypothies(X, y, y_predict):
#     plt.scatter(X, y, color='red')
#     plt.plot(X, y_predict, color='blue')
#     plt.show()


# 测试学习效果
def predict(theta, X):
    # result = 0
    # predict = np.array([1650, 3])  # 设置预测值
    # norm_predict = (predict - mu) / sigma
    # final_predict = np.hstack((np.ones((1)), norm_predict))
    result = np.dot(X, theta)
    return result


# 测试线性回归
def testRegression():
    linearRegression(0.01, 500)


# 开始训练
def linearRegression(alpah=0.01, num_iters=500):
    print('加载数据...')
    data = load_txt_csv('data.txt', ',')
    X = data[:, 0:-1]
    y = data[:, -1]
    m = len(y)
    col = data.shape[1]

    X, mu, sigma = featureScaling(X)
    plot2D(X)

    X = np.hstack((np.ones((m, 1)), X))

    print('执行梯度下降...')
    theta = np.zeros((col, 1))
    y = y.reshape(-1, 1)
    theta, J_history = gradientDescent(X, y, theta, alpah, num_iters)

    plotJ(J_history, num_iters)
    y_predict = np.rint(predict(theta, X))

    print(y_predict.T, '\n', y.T)
    # return mu, sigma, theta, X


if __name__ == '__main__':
    testRegression()
