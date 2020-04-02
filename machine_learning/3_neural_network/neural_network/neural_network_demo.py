import time

import numpy as np
import scipy.io as scio
import matplotlib.pyplot as plt
from scipy import optimize

def display_data(img_data):
    display_array = None
    m, n = img_data.shape
    width = np.int32(np.round(np.sqrt(n)))  # here width should be 20
    height = np.int32(n / width)  # 400/20=20
    rows = np.int32(np.floor(np.sqrt(m)))  # here row's num should be 10
    cols = np.int32(np.ceil(m / rows))  # 100/10=10
    pad = 1  # 分割线
    display_array = -np.ones((pad + rows * (height + pad), pad + cols * (width + pad)))  # (210, 210)
    sum = 0
    # fill display_array's data from img_data
    for i in range(rows):
        for j in range(cols):
            if sum >= m:
                break
            display_array[pad + i * (height + pad):pad + i * (height + pad) + height, pad + j * (width + pad):pad + j * (width + pad) + width] \
                = img_data[sum, :].reshape(height, width, order='F')
            sum += 1
        if sum >= m:
            break
    plt.imshow(display_array, cmap='gray')
    plt.show()


def randInitializeWeights(L_in, L_out):
    epsilon_init = (6.0/(L_in+L_out))**0.5
    W = np.random.rand(L_out, L_in+1)*2*epsilon_init-epsilon_init
    return W


def sigmoid(z):
    h = np.zeros((len(z), 1))
    h = 1.0/(1.0+np.exp(-z))
    return h

def nnCostFunction(nn_params, input_layer_size, hidden_layer_size, num_labels, X, y, Lambda):
    """正向传播得到神经网络的代价函数"""
    Theta1 = nn_params[0:hidden_layer_size*(input_layer_size+1)].reshape(hidden_layer_size, input_layer_size+1)
    Theta2 = nn_params[hidden_layer_size*(input_layer_size+1):nn_params.shape[0]].reshape(num_labels, hidden_layer_size+1)

    m = X.shape[0]
    """映射0-9"""
    class_y = np.zeros((m, num_labels))
    for i in range(num_labels):
        class_y[:, i] = np.int32(y==i).reshape(1, -1)
    # Theta1_count = Theta1.shape[1]
    # Theta1_x = Theta1[:, 1:Theta1_count]
    # Theta2_count = Theta2.shape[1]
    # Theta2_x = Theta2[:, 1:Theta2_count]
    # term = np.dot(np.transpose(np.vstack((Theta1_x.reshape(-1,1),Theta2_x.reshape(-1,1)))),np.vstack((Theta1_x.reshape(-1,1),Theta2_x.reshape(-1,1))))
    term = np.dot(nn_params.T, nn_params)  # 正则化项Theta^2
    '''实现正向传播'''
    a1 = np.hstack((np.ones((m, 1)), X))  # (5000, 401)
    z2 = np.dot(a1, Theta1.T)
    a2 = sigmoid(z2)
    a2 = np.hstack((np.ones((m, 1)), a2))
    z3 = np.dot(a2, Theta2.T)
    h = sigmoid(z3)

    '''带入公式得到function J'''
    J = -(np.dot(np.transpose(class_y.reshape(-1,1)),np.log(h.reshape(-1,1)))+np.dot(np.transpose(1-class_y.reshape(-1,1)),np.log(1-h.reshape(-1,1)))-Lambda*term/2)/m
    return np.ravel(J)


def sigmoidGradient(z):
    g = sigmoid(z)*(1-sigmoid(z))
    return g


def nnGradient(nn_params, input_layer_size, hidden_layer_size, num_labels, X, y, Lambda):
    length = nn_params.shape[0]
    Theta1 = nn_params[0:hidden_layer_size*(input_layer_size+1)].reshape(hidden_layer_size, input_layer_size+1).copy()
    Theta2 = nn_params[hidden_layer_size*(input_layer_size+1):length].reshape(num_labels, hidden_layer_size+1).copy()
    m = X.shape[0]
    class_y = np.zeros((m, num_labels))
    for i in range(num_labels):
        class_y[:, i] = np.int32(y==i).reshape(1, -1)

    Theta1_count = Theta1.shape[1]
    Theta1_x = Theta1[:, 1:Theta1_count]
    Theta2_count = Theta2.shape[1]
    Theta2_x = Theta2[:, 1:Theta2_count]

    Theta1_grad = np.zeros(Theta1.shape)
    Theta2_grad = np.zeros(Theta2.shape)

    '''正向传播'''
    a1 = np.hstack((np.ones((m, 1)),X))
    z2 = np.dot(a1, Theta1.T)
    a2 = sigmoid(z2)
    a2 = np.hstack((np.ones((m, 1)), a2))
    z3 = np.dot(a2, Theta2.T)
    h = sigmoid(z3)

    '''反向传播'''
    delta3 = np.zeros((m, num_labels))
    delta2 = np.zeros((m, hidden_layer_size))
    for i in range(m):
        delta3[i, :] = h[i, :]-class_y[i, :]
        Theta2_grad = Theta2_grad + np.dot(np.transpose(delta3[i, :].reshape(1, -1)), a2[i, :].reshape(1, -1))
        delta2[i, :] = np.dot(delta3[i, :].reshape(1, -1), Theta2_x)*sigmoidGradient(z2[i, :])
        Theta1_grad = Theta1_grad + np.dot(np.transpose(delta2[i, :].reshape(1, -1)), a1[i, :].reshape(1, -1))

    Theta1[:, 0] = 0
    Theta2[:, 0] = 0

    grad = (np.vstack((Theta1_grad.reshape(-1, 1), Theta2_grad.reshape(-1, 1))) + Lambda * np.vstack(
        (Theta1.reshape(-1, 1), Theta2.reshape(-1, 1)))) / m
    return np.ravel(grad)


def predict(Theta1, Theta2, X):
    m = X.shape[0]
    num_labels = Theta2.shape[0]
    '''正向传播'''
    X = np.hstack((np.ones((m, 1)), X))
    h1 = sigmoid(np.dot(X, Theta1.T))
    h1 = np.hstack((np.ones((m, 1)), h1))
    h2 = sigmoid(np.dot(h1, Theta2.T))

    p = np.array(np.where(h2[0, :]==np.max(h2, axis=1)[0]))
    for i in range(1, m):
        t = np.array(np.where(h2[i, :]==np.max(h2, axis=1)[i]))
        p = np.vstack((p, t))

    return p




def neuralNetwork(input_layer_size, hidden_layer_size, output_layer_size):
    img_data = scio.loadmat('../../2_logistic_regression/logistic_reg_new/data_digits.mat')
    X = img_data['X']  # (m=5000,n=400)
    y = img_data['y']
    # print(X.shape, y.shape)
    m, n = X.shape

    # display 100 digts randomly
    rand_indices = [np.random.randint(0, m) for i in range(100)]
    display_data(X[rand_indices, :])

    Lambda = 1
    initial_Theta1 = randInitializeWeights(input_layer_size, hidden_layer_size)
    initial_Theta2 = randInitializeWeights(hidden_layer_size, output_layer_size)
    initial_nn_params = np.vstack((initial_Theta1.reshape(-1, 1),initial_Theta2.reshape(-1, 1)))

    start = time.time()
    result = optimize.fmin_cg(nnCostFunction, initial_nn_params, fprime=nnGradient,
                                args=(input_layer_size, hidden_layer_size, output_layer_size, X, y, Lambda), maxiter=100)
    print('优化方法执行时间: ', time.time() - start)
    print(result)
    length = result.shape[0]
    Theta1 = result[0:hidden_layer_size*(input_layer_size+1)].reshape(hidden_layer_size, input_layer_size+1)
    Theta2 = result[hidden_layer_size*(input_layer_size+1):length].reshape(output_layer_size, hidden_layer_size+1)
    display_data(Theta1[:, 1:length])
    display_data(Theta2[:, 1:length])

    '''预测'''
    p = predict(Theta1, Theta2, X)
    print('预测准确率为: %f%%'%np.mean(np.float64(p==y.reshape(-1, 1))*100))
    res = np.hstack((p, y.reshape(-1, 1)))
    np.savetxt('predict.csv', res, delimiter=',')


# 初始化调试的theta权重
def debugInitializeWeights(fan_in,fan_out):
    W = np.zeros((fan_out,fan_in+1))
    x = np.arange(1,fan_out*(fan_in+1)+1)
    W = np.sin(x).reshape(W.shape)/10
    return W


def checkGradient(Lambda=0):
    # 梯度检测
    input_layer_size = 3
    hidden_layer_size = 5
    num_labels = 3
    m = 5
    initial_Theta1 = debugInitializeWeights(input_layer_size, hidden_layer_size)
    initial_Theta2 = debugInitializeWeights(hidden_layer_size, num_labels)
    X = debugInitializeWeights(input_layer_size-1, m)
    y = 1+ np.transpose(np.mod(np.arange(1, m+1), num_labels))
    y = y.reshape(-1, 1)
    nn_params = np.vstack((initial_Theta1.reshape(-1, 1), initial_Theta2.reshape(-1, 1)))
    grad = nnGradient(nn_params, input_layer_size, hidden_layer_size, num_labels, X, y, Lambda)

    num_grad = np.zeros((nn_params.shape[0]))
    step = np.zeros((nn_params.shape[0]))
    e = 1e-4
    for i in range(nn_params.shape[0]):
        step[i] = e
        loss1 = nnCostFunction(nn_params-step.reshape(-1, 1), input_layer_size, hidden_layer_size, num_labels, X, y, Lambda)
        loss2 = nnCostFunction(nn_params+step.reshape(-1, 1), input_layer_size, hidden_layer_size, num_labels, X, y, Lambda)
        num_grad[i] = (loss2-loss1) / (2*e)
        step[i] = 0

    res = np.hstack((num_grad.reshape(-1, 1), grad.reshape(-1, 1)))
    print(res)


def testNeuralNetwork():
    checkGradient()
    neuralNetwork(400, 25, 10)


if __name__ == '__main__':
    testNeuralNetwork()
