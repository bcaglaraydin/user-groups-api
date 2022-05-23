from flask import Blueprint

user = Blueprint("user", __name__, url_prefix="/api/user")


@user.post('/add')
def register():
    return "User Created"


@user.get('/')
def getAll():
    return {"users": []}
