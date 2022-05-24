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


@group.get('/')
def getAllGroups():
    all_groups = Group.query.all()

    output = []

    for user in all_groups:
        group_data = {}
        group_data['name'] = user.name
        output.append(group_data)
    return jsonify({'groups': output}), status.HTTP_200_OK
