class Config:
    FLASK_APP = "src"
    SQLALCHEMY_DATABASE_URI = "sqlite:///users.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProdConfig(Config):
    ENV = "production"
    DEBUG = False
    TESTING = False


class DevConfig(Config):
    ENV = "development"
    DEBUG = True
    TESTING = True
