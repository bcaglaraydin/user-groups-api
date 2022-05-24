from flask import Blueprint, request, jsonify
from flask_api import status


from src.database import Group, db

group = Blueprint("group", __name__, url_prefix="/api/group")


@group.post('/create')
def create():
    name = request.json['name']

    if Group.query.filter_by(name=name).first() is not None:
        return jsonify({'error': "Name already exists"}), status.HTTP_409_CONFLICT

    group = Group(name=name)
    db.session.add(group)
    db.session.commit()

    return jsonify({
        'message': "Group created",
        'group': {
            'name': name
        }
    }), status.HTTP_201_CREATED
