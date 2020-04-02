#! /usr/bin/env python
# encoding: utf-8
import numpy as np
import scipy.io as spio
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import pca


def plot_data_2d(X, marker):
    plt.plot(X[:, 0], X[:, 1], marker)
    return plt


def PCA_2d_example():
    data = spio.loadmat('data.mat')
    X = data['X']
    plt = plot_data_2d(X, 'bo')
    plt.title('original data')
    plt.show()

    scaler = StandardScaler()
    scaler.fit(X)
    X_train = scaler.transform(X)
    plot_data_2d(X_train, 'bo')
    plt.axis('square')
    plt.title('scaler data')
    plt.show()

    # 拟合数据
    k = 1
    model = pca.PCA(n_components=k).fit(X_train)
    Z = model.transform(X_train)

    # 数据恢复
    Ureduce = model.components_
    X_rec = np.dot(Z, Ureduce)
    plot_data_2d(X_rec, 'bo')
    plt.axis('square')
    plt.title('recover data')
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
    height = np.int32(n / width)
    rows_count = np.int32(np.floor(np.sqrt(m)))  # 行的个数
    cols_count = np.int32(np.ceil(m / rows_count))  # 列的个数
    pad = 1  # 图片之间分割线
    display_array = -np.ones((pad + rows_count * (height + pad), pad + cols_count * (width + pad)))
    sum = 0
    for i in range(rows_count):
        col_start, col_end = (pad + i * (height + pad), pad + i * (height + pad) + height)
        for j in range(cols_count):
            max_val = np.max(np.abs(imgData[sum, :]))
            row_start, row_end = (pad + j * (width + pad), pad + j * (width + pad) + width)
            display_array[col_start: col_end, row_start: row_end] \
                = imgData[sum, :].reshape(height, width, order='F') / max_val
            sum += 1
    plt.imshow(display_array, cmap='gray')
    plt.show()


def PCA_face_example():
    # 加载图片数据
    data_image = spio.loadmat('data_faces.mat')
    X = data_image['X']
    # 显示降维前的数据
    display_imageData(X[0:100, :])
    # 特征缩放
    scaler = StandardScaler()
    scaler.fit(X)
    X_train = scaler.transform(X)
    # 进行PCA降维
    k = 100
    model = pca.PCA(n_components=k).fit(X_train)
    Z = model.transform(X_train)
    print(Z.shape)
    Ureduce = model.components_
    display_imageData(Ureduce[0:36, :])
    X_rec = np.dot(Z, Ureduce)
    display_imageData(X_rec[0:100, :])


if __name__ == '__main__':
    # PCA_2d_example()
    PCA_face_example()
