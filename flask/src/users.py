from email import message
from statistics import median_low
from flask import Blueprint, request, jsonify
from flask_api import status
from sqlalchemy import null
from werkzeug.security import generate_password_hash
import validators

from src.database import User, Group, db

user = Blueprint("user", __name__, url_prefix="/api/user")


@user.post('/create')
def createUser():
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
            'id': user.id,
            'name': name,
            'email': email
        }
    }), status.HTTP_201_CREATED


@user.get('/')
def getAllUsers():
    all_users = User.query.all()

    output = []
    for user in all_users:
        user_data = {}
        user_data['id'] = user.id
        user_data['name'] = user.name
        user_data['email'] = user.email
        output.append(user_data)

    return jsonify({'users': output}), status.HTTP_200_OK


@user.get('/<id>')
def getUser(id):
    user = User.query.filter_by(id=id).first()

    if not user:
        return jsonify({'error': 'User not found!'}), status.HTTP_404_NOT_FOUND

    user_data = {}
    user_data['id'] = user.id
    user_data['name'] = user.name
    user_data['email'] = user.email

    return jsonify({'user': user_data}), status.HTTP_200_OK


@user.put('/<id>')
def editUser(id):

    user = User.query.filter_by(id=id).first()

    if not user:
        return jsonify({'error': 'User not found!'}), status.HTTP_404_NOT_FOUND

    _name = request.json['name']
    _email = request.json['email']
    _password = request.json['password']

    if len(_password) < 6:
        return jsonify({'error': "Password is too short"}), status.HTTP_400_BAD_REQUEST

    if not validators.email(_email):
        return jsonify({'error': "Email is not valid"}), status.HTTP_400_BAD_REQUEST

    if User.query.filter_by(email=_email).first() is not None and user.email != _email:
        return jsonify({'error': "Email is taken"}), status.HTTP_409_CONFLICT

    if User.query.filter_by(name=_name).first() is not None and user.name != _name:
        return jsonify({'error': "Name already exists"}), status.HTTP_409_CONFLICT

    pwd_hash = generate_password_hash(_password)

    user.name = _name
    user.email = _email
    user.password = pwd_hash

    db.session.commit()

    return jsonify({
        'message': "User updated",
        'user': {
            'id': user.id,
            'name': _name,
            'email': _email
        }
    }), status.HTTP_200_OK


@user.post('/add')
def addToGroup():
    user_id = request.json["user_id"]
    group_id = request.json["group_id"]

    user = User.query.filter_by(id=user_id).first()
    group = Group.query.filter_by(id=group_id).first()

    if not user:
        return jsonify({'error': 'User not found!'}), status.HTTP_404_NOT_FOUND

    if not group:
        return jsonify({'error': 'Group not found!'}), status.HTTP_404_NOT_FOUND

    if user.group_id == group_id:
        return jsonify({'error': 'User is already in this group!'}), status.HTTP_409_CONFLICT

    user.group_id = group_id
    db.session.commit()

    return jsonify({
        'message': "User " + user.name + " added to group " + group.name
    }), status.HTTP_200_OK


@user.post('/remove')
def removeFromGroup():
    user_id = request.json["user_id"]
    group_id = request.json["group_id"]

    user = User.query.filter_by(id=user_id).first()
    group = Group.query.filter_by(id=group_id).first()

    if not user:
        return jsonify({'error': 'User not found!'}), status.HTTP_404_NOT_FOUND

    if user.group_id != group_id:
        return jsonify({'error': 'User does not belong to this group!'}), status.HTTP_404_NOT_FOUND

    user.group_id = None
    db.session.commit()

    return jsonify({
        'message': "User " + user.name + " removed from group " + group.name
    }), status.HTTP_200_OK


@user.delete('/<id>')
def deleteUser(id):
    user = User.query.filter_by(id=id).first()

    if not user:
        return jsonify({'error': 'User not found!'}), status.HTTP_404_NOT_FOUND

    db.session.delete(user)
    db.session.commit()

    return jsonify({}), status.HTTP_204_NO_CONTENT
