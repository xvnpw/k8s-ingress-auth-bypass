from flask import Flask, Response, request
from http import HTTPStatus
import sys

app = Flask(__name__)

@app.route('/verify')
def verify():
    print(request.headers, file=sys.stderr)
    api_key = request.headers.get('X-Api-Key')
    request_redirect = request.headers.get('X-Auth-Request-Redirect')

    if request_redirect and request_redirect.startswith("/public-service/"):
        return Response(status = HTTPStatus.NO_CONTENT)

    if api_key == "secret-api-key":  
        return Response(status = HTTPStatus.NO_CONTENT)

    return Response(status = HTTPStatus.UNAUTHORIZED)
