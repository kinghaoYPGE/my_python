import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler


def plot_data(X, y):
    pos = np.where(y == 1)
    neg = np.where(y == 0)
    plt.plot(X[pos, 0], X[pos, 1], 'ro')
    plt.plot(X[neg, 0], X[neg, 1], 'bo')
    plt.show()


def logisticRegression():
    data = np.loadtxt('data1.txt', delimiter=',', dtype=np.float64)
    X = data[:, :-1]
    y = data[:, -1]
    # plot_data(X, y)  # 经过观察，发现决策边界时一个曲线
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    scaler = StandardScaler()
    scaler.fit(X_train)
    scaler.fit_transform(X_train)
    scaler.fit_transform(X_test)
    model = LogisticRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print('预测准确率为:%f%%' % np.mean(np.float64(y_pred == y_test) * 100))


def testLogisticRegression():
    logisticRegression()


if __name__ == '__main__':
    testLogisticRegression()
