from flask import request
from hello import app

with app.test_request_context('/url', method='GET') as test:
    assert request.path == '/url'
    assert request.method == 'GET'
