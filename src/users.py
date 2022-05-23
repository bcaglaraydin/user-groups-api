from flask import Blueprint
from flask_api import status

user = Blueprint("user", __name__, url_prefix="/api/user")


@user.post('/add')
def register():
    return "User Created"


@user.get('/')
def getAll():
    return {"users": []}, status.HTTP_200_OK
