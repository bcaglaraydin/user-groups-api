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
            'id': group.id,
            'name': name
        }
    }), status.HTTP_201_CREATED


@group.get('/')
def getAllGroups():
    all_groups = Group.query.all()

    output = []

    for group in all_groups:
        group_data = {}
        group_data['id'] = group.id
        group_data['name'] = group.name
        output.append(group_data)
    return jsonify({'groups': output}), status.HTTP_200_OK


@group.get('/<id>')
def getGroup(id):
    group = Group.query.filter_by(id=id).first()

    if not group:
        return jsonify({'error': 'Group not found!'}), status.HTTP_404_NOT_FOUND

    group_data = {}
    group_data['id'] = group.id
    group_data['name'] = group.name

    return jsonify({'group': group_data}), status.HTTP_200_OK


@group.patch('/<id>')
@group.put('/<id>')
def editGroup(id):

    group = Group.query.filter_by(id=id).first()

    if not group:
        return jsonify({'error': 'Group not found!'}), status.HTTP_404_NOT_FOUND

    _name = request.json['name']

    if Group.query.filter_by(name=_name).first() is not None and group.name != _name:
        return jsonify({'error': "Name already exists"}), status.HTTP_409_CONFLICT
    group.name = _name

    db.session.commit()

    return jsonify({
        'message': "Group updated",
        'group': {
            'id': group.id,
            'name': _name
        }
    }), status.HTTP_200_OK
