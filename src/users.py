from this import d
from flask import Blueprint, request, jsonify
from flask_api import status
from werkzeug.security import check_password_hash, generate_password_hash
import validators

from src.database import User, db

user = Blueprint("user", __name__, url_prefix="/api/user")


@user.post('/create')
def register():
    name = request.json['name']
    email = request.json['email']
    password = request.json['password']

    if len(password) < 6:
        return jsonify({'error': "Password is too short"}), status.HTTP_400_BAD_REQUEST

    if not validators.email(email):
        return jsonify({'error': "Email is not valid"}), status.HTTP_400_BAD_REQUEST

    if User.query.filter_by(email=email).first() is not None:
        return jsonify({'error': "Email is taken"}), status.HTTP_409_CONFLICT

    if User.query.filter_by(name=name).first() is not None:
        return jsonify({'error': "Name already exists"}), status.HTTP_409_CONFLICT

    pwd_hash = generate_password_hash(password)

    user = User(name=name, password=pwd_hash, email=email)
    db.session.add(user)
    db.session.commit()

    return jsonify({
        'message': "User created",
        'user': {
            'name': name,
            'email': email
        }
    }), status.HTTP_201_CREATED


@user.get('/')
def getAll():
    return {"users": []}, status.HTTP_200_OK
