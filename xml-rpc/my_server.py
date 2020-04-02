from xmlrpc.server import SimpleXMLRPCServer


def add(x, y):
    return x + y


def subtract(x, y):
    return x - y


def multiply(x, y):
    return x * y


def divide(x, y):
    return x / y


if __name__ == '__main__':
    server = SimpleXMLRPCServer(('0.0.0.0', 8000))
    print('listening on port 8000...')
    server.register_multicall_functions()
    server.register_function(add, 'add')
    server.register_function(subtract, 'subtract')
    server.register_function(multiply, 'multiply')
    server.register_function(divide, 'divide')
    server.serve_forever()
