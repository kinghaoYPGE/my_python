import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.io as scio
import scipy.optimize as opt


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


def display_data(imgData):
    sum = 0
    pad = 1
    display_array = -np.ones((pad + 10 * (20 + pad), pad + 10 * (20 + pad)))  # (211, 211)
    """
        下面的二维循环可能不是很容易理解:
        其实很简单，就是将前面得到的像素内容填充到我们刚刚定义的display_array中
        然后通过plt显示出来
    """
    for i in range(10):
        for j in range(10):
            display_array[pad + i * (20 + pad):pad + i * (20 + pad) + 20,
            pad + j * (20 + pad):pad + j * (20 + pad) + 20] \
                = (imgData[sum, :].reshape(20, 20, order="F"))
            sum += 1
    plt.imshow(display_array, cmap='gray')
    # plt.axis('off')
    plt.show()


def oneVsAll(X, y, num_labers, Lambda):
    """
    得到每个分类(0-9)的theta
    :param X:
    :param y:
    :param num_labers:
    :param Lambda:
    :return:
    """
    m, n = X.shape
    all_theta = np.zeros((n + 1, num_labers))  # 初始化theta, n+1是因为要补一个theta0
    X = np.hstack((np.ones((m, 1)), X))  # 补上X0=1
    class_y = np.zeros((m, num_labers))  # 用0, 1来映射0-9 y
    initial_theta = np.zeros((n + 1, 1))  # 先初始化一个分类的theta

    # 对y进行映射 规则: 0->100000000,1->01000000...
    for i in range(num_labers):
        class_y[:, i] = np.int32(y == i).reshape(1, -1)  # 利用numpy的广播将原来的y和0到1进行比较, 相等就显示1, 否则显示0

    # 遍历每个分类, 计算出对应的theta
    for i in range(num_labers):
        # 这里我们使用scipy的优化方法进行求解, 这里注意class_y[:, i]的用法就是oneVsAll
        result = opt.fmin_bfgs(costFunction, initial_theta,
                               fprime=gradient, args=(X, class_y[:, i], Lambda))
        all_theta[:, i] = result.reshape(1, -1)

    all_theta = np.transpose(all_theta)
    return all_theta


def predict_oneVsAll(all_theta, X):
    """
    通过已得到的theta进行测试，看是否拟合
    :param all_theta:
    :param X:
    :return:
    """
    m = X.shape[0]
    num_labers = all_theta.shape[0]
    p = np.zeros((m, 1))
    X = np.hstack((np.ones((m, 1)), X))
    h = sigmoid(np.dot(X, all_theta.T))  # (5000, 10)

    # 然后将h转化成0-9的数字
    p = np.array(np.where(h[0, :] == np.max(h, axis=1)[0]))
    for i in range(1, m):
        t = np.array(np.where(h[i, :] == np.max(h, axis=1)[i]))
        p = np.vstack((p, t))
    return p



def logReg_OneVsAll():
    data = scio.loadmat('data_digits.mat')
    X = data['X']
    y = data['y']
    m, n = X.shape  # (5000, 400)这里的400对应的是像素, 5000是数据集, 0-500是0,500-1000是1...以此类推
    num_labers = 10

    # 这里就不下载已有的数据集图片了，我们根据像素随机画100个数字
    rand_indices = [np.random.randint(x - x, m) for x in range(100)]
    display_data(X[rand_indices, :])

    Lambda = 0.1  # 正则化系数
    all_theta = oneVsAll(X, y, num_labers, Lambda)

    # 进行测试
    p = predict_oneVsAll(all_theta, X)
    print('预测准确率为%f%%' % np.mean(np.float64(p == y.reshape(-1, 1)) * 100))


def testLogReg_OneVSAll():
    logReg_OneVsAll()


if __name__ == '__main__':
    testLogReg_OneVSAll()
