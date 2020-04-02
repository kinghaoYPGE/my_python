#! /usr/bin/env python
# encoding: utf-8
import numpy as np
from scipy import io as spio
import matplotlib.pyplot as plt


def featureNormalize(X):
    """
    :param X:
    :return: （每一个数据-当前列的均值）/ 当前列的标准差（max-min）
    """
    n = X.shape[1]
    mu = np.zeros((1, n))
    sigma = np.zeros((1, n))

    mu = np.mean(X, axis=0)  # 求每一列的均值
    sigma = np.std(X, axis=0)  # 求每一列的标准差

    X = (X - mu) / sigma
    return X, mu, sigma


def projectData(X_norm, U, k):
    Z = np.zeros((X_norm.shape[0], k))
    U_reduce = U[:, 0:k]
    Z = np.dot(X_norm, U_reduce)  # (50, 2)*(2, 1)
    return Z


def recoverData(Z, U, k):
    X_rec = np.zeros((Z.shape[0], U.shape[0]))
    U_reduce = U[:, 0:k]
    X_rec = np.dot(Z, np.transpose(U_reduce))  # 这里是近似值
    return X_rec


def plot_data_2d(X, marker):
    plt.plot(X[:, 0], X[:, 1], marker)
    return plt


def drawline(plt, p1, p2, line_type):
    plt.plot(np.array([p1[0], p2[0]]), np.array([p1[1], p2[1]]), line_type)


def PCA_2D():
    data_2d = spio.loadmat('data.mat')
    X = data_2d['X']
    m = X.shape[0]
    # plt = plot_data_2d(X, 'bo')
    # plt.show()

    X_copy = X.copy()
    X_norm, mu, sigma = featureNormalize(X_copy)
    Sigma = np.dot(np.transpose(X_norm), X_norm) / m
    U, S, V = np.linalg.svd(Sigma)
    plt = plot_data_2d(X, 'bo')
    drawline(plt, mu, mu + S[0] * (U[:, 0]), 'r-')

    plt.axis('square')
    plt.show()
    k = 1  # from 2d to 1d

    Z = projectData(X_norm, U, k)  # 进行降维
    print(Z.shape)  # (50, 1)
    X_rec = recoverData(Z, U, k)  # 恢复数据
    plt = plot_data_2d(X_norm, 'bo')
    plot_data_2d(X_rec, 'ro')

    for i in range(X_norm.shape[0]):
        drawline(plt, X_norm[i, :], X_rec[i, :], '--k')

    plt.axis('square')
    plt.show()


def display_imageData(imgData):
    """
    :param imgData: 这里的img是100x1024的，我们要转成320x320的矩阵
    :return:
    """
    # plt.imshow(imgData[0:1, :].reshape((-1, 32)), cmap='gray')
    # plt.axis('off')
    m, n = imgData.shape
    width = np.int32(np.round(np.sqrt(n)))  # here is sqrt(1024) = 32
    height = np.int32(n/width)
    rows_count = np.int32(np.floor(np.sqrt(m)))  # 行的个数
    cols_count = np.int32(np.ceil(m/rows_count))  #列的个数
    pad = 1  # 图片之间分割线
    display_array = -np.ones((pad+rows_count*(height+pad), pad+cols_count*(width+pad)))
    sum = 0
    for i in range(rows_count):
        col_start, col_end = (pad+i*(height+pad), pad+i*(height+pad)+height)
        for j in range(cols_count):
            max_val = np.max(np.abs(imgData[sum, :]))
            row_start, row_end = (pad+j*(width+pad), pad+j*(width+pad)+width)
            display_array[col_start: col_end, row_start: row_end] \
                = imgData[sum, :].reshape(height, width, order='F')/max_val
            sum += 1
    plt.imshow(display_array, cmap='gray')
    plt.show()


def PCA_faceImage():
    print(u'load image data...')
    data_image = spio.loadmat('data_faces.mat')
    X = data_image['X']
    # 只显示前100张图片 px是32x32
    display_imageData(X[0: 100, :])
    m = X.shape[0]
    print(u'run PCA...')
    X_norm, mu, sigma = featureNormalize(X)
    Sigma = np.dot(np.transpose(X_norm), X_norm)
    U,S,V = np.linalg.svd(Sigma)
    display_imageData(U[:, 0:36].T)
    print(u'dimensionlity reduction...')
    k = 100  # from 32*32=1024d to 100d
    Z = projectData(X_norm, U, k)
    print(u'投影之后的大小%d %d' % Z.shape)
    print(u'显示降维之后的数据...')
    X_rec = recoverData(Z, U, k)
    display_imageData(X_rec[0:100, :])




if __name__ == '__main__':
    # PCA_2D()
    PCA_faceImage()
