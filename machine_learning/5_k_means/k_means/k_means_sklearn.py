#! /usr/bin/env python
# encoding: utf-8
from scipy import io as spio
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


def kMeans():
    data = spio.loadmat('data.mat')
    X = data['X']
    model = KMeans(n_clusters=3).fit(X)
    centroids = model.cluster_centers_
    plt.scatter(X[:, 0], X[:, 1])
    plt.plot(centroids[:, 0], centroids[:, 1], 'r^', markersize=10)
    plt.show()


if __name__ == '__main__':
    kMeans()
