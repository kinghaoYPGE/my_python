from xmlrpc.client import ServerProxy


proxy = ServerProxy('http://localhost:8000')

r1 = proxy.add(7, 3)
r2 = proxy.subtract(7, 3)
r3 = proxy.multiply(7, 3)
r4 = proxy.divide(7, 3)

print(r1, r2, r3, r4)
