import numpy as np
import scipy.io as scio
import matplotlib.pyplot as plt
from sklearn import svm


def plot_data(X, y):
    plt.figure(figsize=(10, 8))  # 设置画布大小
    pos = np.where(y == 1)  # 找到y=1的位置
    neg = np.where(y == 0)  # 找到y=0的位置
    p1 = plt.plot(np.ravel(X[pos, 0]), np.ravel(X[pos, 1]), 'ro', markersize=8)
    p2 = plt.plot(np.ravel(X[neg, 0]), np.ravel(X[neg, 1]), 'bo', markersize=8)
    plt.xlabel('x1')
    plt.ylabel('x2')
    plt.legend([p1, p2], ['y==1', 'y==2'])
    return plt


def plot_decisionBoundary(X, y, model, class_='linear'):
    plt = plot_data(X, y)
    if class_ == 'linear':
        w = model.coef_
        b = model.intercept_
        xp = np.linspace(np.min(X[:, 0]), np.max(X[:, 0]), 100)
        yp = -(w[0, 0] * xp + b) / w[0, 1]
        plt.plot(xp, yp, 'b-', linewidth=2.0)
        plt.show()
    else:
        x_1 = np.transpose(np.linspace(np.min(X[:, 0]), np.max(X[:, 0]), 100).reshape(1, -1))
        x_2 = np.transpose(np.linspace(np.min(X[:, 1]), np.max(X[:, 1]), 100).reshape(1, -1))
        X1, X2 = np.meshgrid(x_1, x_2)
        vals = np.zeros(X1.shape)
        for i in range(X1.shape[1]):
            this_X = np.hstack((X1[:, i].reshape(-1, 1), X2[:, i].reshape(-1, 1)))
            vals[:, i] = model.predict(this_X)

        plt.contour(X1, X2, vals, [0, 1], color='blue')
        plt.show()


def SVM():
    #  线性分类
    data1 = scio.loadmat('data1.mat')
    X = data1['X']
    y = data1['y']
    y = np.ravel(y)
    # plot_data(X, y)
    model = svm.SVC(C=1.0, kernel='linear').fit(X, y)
    plot_decisionBoundary(X, y, model)

    #  非线性分类
    data2 = scio.loadmat('data2.mat')
    X = data2['X']
    y = data2['y']
    y = np.ravel(y)
    model = svm.SVC(gamma=100).fit(X, y)
    plot_decisionBoundary(X, y, model, class_='nonlinear')


if __name__ == '__main__':
    SVM()
