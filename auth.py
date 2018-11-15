from flask import Flask, request, Response
from functools import wraps

app = Flask(__name__)
app.secret_key = "Dev Key"

## Auth
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth:
            return authenticate()

        if not check_auth(auth.username, auth.password):
            return authenticate()

        return f(*args, **kwargs)

    return decorated


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        "Could not verify your access level for that URL.\nYou have to login with proper credentials",
        401,
        {"WWW-Authenticate": 'Basic realm="Login Required"'},
    )


def check_auth(username, password):
    """Checks that user creds are valid."""
    return username == "admin" and password == "secret"


# Routes
@app.route("/")
@requires_auth
def hello():
    return "Hello World!"


if __name__ == "__main__":
    app.run()
