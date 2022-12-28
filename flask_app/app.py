# flask_app/app.py
import http
import os

from flask import Flask, jsonify
from flask_pydantic import validate

from db import db, init_db
from db_models import User
from forms import LoginForm

app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config["SECRET_KEY"] = SECRET_KEY

init_db(app)
app.app_context().push()
db.create_all()


@app.route("/hello-world")
def hello_world():
    return f"Hello, World!"


@app.route("/api/v1/auth/login", methods=["POST"])
@validate(body=LoginForm)
def check_login_password(body: LoginForm):
    user = User.query.filter_by(email=body.email).one_or_none()

    if not (user and user.check_password(body.password)):
        return jsonify({"msg": "Wrong email or password"}), http.HTTPStatus.UNAUTHORIZED

    print("Success authorization!")

    # TODO ("Put to DB: location, refresh_token, time")
    return jsonify({"msg": "Success authorization!"}), http.HTTPStatus.OK


@app.route("/api/v1/auth/registration", methods=["POST"])
@validate()
def registration(body: LoginForm):
    user = User(email=body.email)
    user.set_password(body.password)

    if User.query.filter_by(email=body.email).one_or_none():
        return (
            jsonify({"msg": "The email is already registered"}),
            http.HTTPStatus.UNAUTHORIZED,
        )

    with app.app_context():
        db.session.add(user)
        db.session.commit()

    return jsonify({"msg": "Thank you for registration!"}), http.HTTPStatus.OK


@app.route("/api/v1/auth/refresh-tokens", methods=["POST"])
def refresh_token():
    pass


@app.route("/api/v1/auth/logout", methods=["POST"])
def logout():
    pass


if __name__ == "__main__":
    app.run(debug=True)
