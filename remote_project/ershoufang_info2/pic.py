import numpy
from matplotlib import pyplot as plt

price, size = numpy.loadtxt('houses.csv', delimiter='|', usecols=(1,2,), unpack=True)
print(price)
print(size)

# 求价格和面积的平均值
price_mean = numpy.mean(price)
size_mean = numpy.mean(size)

print('平均房价： %s万'%round(price_mean, 2))

plt.figure()
plt.subplot(211)
plt.title('/ 10000RMB')
plt.hist(price, bins=20)

plt.subplot(212)
plt.xlabel('/ m**2')
plt.hist(size, bins=20)

plt.figure(2)
plt.plot(price)
plt.show()