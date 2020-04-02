import numpy as np
import pandas as pd
import scipy.io as scio
# from sklearn import svm
from sklearn.linear_model import LogisticRegression


def logisticRegression_OneVsAll():
    data = scio.loadmat('data_digits.mat')
    X = data['X']
    y = data['y']
    y = np.ravel(y)
    model = LogisticRegression()
    model.fit(X, y)
    p = model.predict(X)
    print('预测准确率为%f%%' % np.mean(np.float64(p == y) * 100))



if __name__ == '__main__':
    logisticRegression_OneVsAll()
