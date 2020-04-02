import numpy as np
import matplotlib.pyplot as plt
import scipy.io as scio
from scipy import misc


def findClosetcentroids(X, inital_centroids):
    """
    计算每条数据到哪个中心最近
    :param X:
    :param inital_centroids:
    :return:
    """
    m = X.shape[0]
    k = inital_centroids.shape[0]
    dis = np.zeros((m, k))  # 存储每个样本到k个类的距离
    idx = np.zeros((m, 1))

    for i in range(m):
        for j in range(k):
            item = X[i, :] - inital_centroids[j, :]
            dis[i, j] = np.dot(item.reshape(1, -1), item.reshape(-1, 1))

    dummy, idx = np.where(dis == np.min(dis, axis=1).reshape(-1, 1))
    return idx[0:dis.shape[0]]


def computeCentroids(X, idx, k):
    """
    通过得到的
    :param X:
    :param idx:
    :param k:
    :return:
    """
    n = X.shape[1]
    centroids = np.zeros((k, n))
    for i in range(k):
        centroids[i, :] = np.mean(X[np.ravel(idx == i), :], axis=0).reshape(1, -1)
    return centroids


def plotProcessKMeans(X, centroids, previous_centroids):
    plt.scatter(X[:, 0], X[:, 1])
    plt.plot(previous_centroids[:, 0], previous_centroids[:, 1],
             'rx', markersize=10, linewidth=5.0)
    plt.plot(centroids[:, 0], centroids[:, 1], 'bx', markersize=10, linewidth=5.0)
    for j in range(centroids.shape[0]):
        p1 = centroids[j, :]
        p2 = previous_centroids[j, :]
        plt.plot([p1[0], p2[0]], [p1[1], p2[1]], '->', linewidth=2.0)
    return plt


def runMeans(X, inital_centroids, max_iters, plot_precess):
    m, n = X.shape
    k = inital_centroids.shape[0]
    centroids = inital_centroids  # 记录当前类中心
    previous_centroids = centroids
    idx = np.zeros((m, 1))  # 每条数据属于哪个类

    for i in range(max_iters):
        # 判断当前类属于哪个中心
        idx = findClosetcentroids(X, centroids)
        if plot_precess:
            plt = plotProcessKMeans(X, centroids, previous_centroids)
            previous_centroids = centroids  # 重置
        # 重新得到cluster centroids
        centroids = computeCentroids(X, idx, k)
    if plot_precess:
        plt.show()

    return centroids, idx


def kMeansInitCentroids(X, k):
    """
    初始化 cluster centroids
    :param X:
    :param k:
    :return:
    """
    m = X.shape[0]
    centroids = np.zeros((k, X.shape[1]))
    m_arr = np.arange(0, m)
    np.random.shuffle(m_arr)
    rand_indices = m_arr[:k]
    centroids = X[rand_indices, :]

    return centroids


def kmeans():
    '''data = scio.loadmat('data.mat')
    X = data['X']
    k = 3
    # 初始化聚类中心
    inital_centroids = np.array([[3, 3], [6, 2], [8, 5]])
    max_iters = 10
    # 执行聚类算法
    runMeans(X, inital_centroids, max_iters, True)'''

    """
    实现图片压缩
    """
    print('K-Means 压缩图片执行...')
    img_data = misc.imread('bird.png')
    img_data = img_data / 255.0  # 像素值映射到0-1
    img_size = img_data.shape  # (128, 128, 3)
    X = img_data.reshape(img_size[0] * img_size[1], 3)
    k = 16
    max_iters = 5
    inital_centroids = kMeansInitCentroids(X, k)
    centroids, idx = runMeans(X, inital_centroids, max_iters, False)
    idx = findClosetcentroids(X, centroids)
    print(centroids.shape, idx.shape)

    X_recoverd = centroids[idx, :].reshape(img_size[0], img_size[1], 3)
    print(X_recoverd.shape)
    plt.subplot(1, 2, 1)
    plt.imshow(img_data)
    plt.title('image compression before')
    plt.subplot(1, 2, 2)
    plt.imshow(X_recoverd)
    plt.title('image compression after')
    plt.show()
    print('图片压缩结束...')


if __name__ == '__main__':
    kmeans()
