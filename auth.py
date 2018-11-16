from flask import Flask, request, Response
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import bcrypt
import os

app = Flask(__name__)
app.secret_key = "Dev Key"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    app.root_path, "auth.db"
)

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(72))

    @staticmethod
    def hash_password(plain_text):
        return bcrypt.hashpw(plain_text.encode('utf-8'), bcrypt.gensalt())

    def check_password(self, plain_text):
        return bcrypt.checkpw(plain_text.encode('utf-8'), self.password)


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
    u = User.query.filter_by(username=username).first()
    if not u:
        return False
    return username == u.username and u.check_password(password)



# Routes
@app.route("/")
@requires_auth
def hello():
    return "Hello World!"


@app.route("/other/")
@requires_auth
def other():
    return "Hello World from somewhere else!"


# CLI
@app.cli.command("init")
def init_db():
    """Initialize database with Users"""
    db.drop_all()
    db.create_all()

    db.session.add(User(username="admin", password=User.hash_password("secret")))
    db.session.add(User(username="tow", password=User.hash_password("secret")))

    db.session.commit()

    print("Added users and initialized database.")


if __name__ == "__main__":
    app.run()
