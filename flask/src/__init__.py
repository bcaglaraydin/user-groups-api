from flask import Flask, jsonify
from flask_api import status
from src.users import user
from src.groups import group
from src.database import db
from flask_swagger_ui import get_swaggerui_blueprint
from src.config import DevConfig, ProdConfig


app = Flask(__name__, instance_relative_config=True)

app.config.from_object(ProdConfig())

SWAGGER_URL = '/docs'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "user-groups-api"
    }
)

app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
db.app = app
db.init_app(app)
db.drop_all()
db.create_all()
app.register_blueprint(user)
app.register_blueprint(group)


@app.errorhandler(status.HTTP_500_INTERNAL_SERVER_ERROR)
def handle_500(e):
    return jsonify({"error": "Server error"}), status.HTTP_500_INTERNAL_SERVER_ERROR
