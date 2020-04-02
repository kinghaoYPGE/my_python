import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt


def linear_regression():
    print('加载数据...')
    data = np.loadtxt('data.txt', delimiter=',')
    X = data[:, 0:-1]
    y = data[:, -1]

    scaler = StandardScaler()
    scaler.fit(X)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)

    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    return X_train, X_test, y_train, y_test, y_pred


if __name__ == '__main__':
    X_train, X_test, y_train, y_test, y_pred = linear_regression()
    print(y_test, y_pred)
    plt.scatter(y_test, y_pred, color='blue')
