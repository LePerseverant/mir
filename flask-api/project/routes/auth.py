from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, unset_jwt_cookies, jwt_required
from ..models.user import User
from ..db import db
from werkzeug.security import generate_password_hash 

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.post("/register")
def sign_up():

    data = request.get_json()
    if data is None:
        return jsonify({ "error": "email and password are required."}), 400

    email = data.get("email")
    password = data.get("password")

    user = User(email=email)
    user.password = password

    db.session.add(user)
    db.session.commit()

    return jsonify({ "message": "user registered successfully" }), 201


@bp.post("/login")
def sign_in():

    data = request.get_json()
    if data is None:
        return jsonify({ "error": "email and password are required."}), 400

    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({ "error": "invalid email" }), 401

    if not user.check_password(password):
        return jsonify({ "error": "invalid password"}), 401

    token = create_access_token(identity=email)
    return jsonify({ "data": { "token": token } })


@bp.get("/logout")
def sign_out():
    response = jsonify({ "message": "logout successful."})
    unset_jwt_cookies(response)
    return response


