import os
from environmentals import SECRET_KEY

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Config:
    SECRET_KEY = SECRET_KEY
    DEBUG = False
    TESTING = False

    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
    SANITIZED_FOLDER = os.path.join(BASE_DIR, "sanitized")

    MAX_CONTENT_LENGTH = 10 * 1024 * 1024
    ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}
    TEMPLATES_AUTO_RELOAD = True


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


class TestingConfig(Config):
    TESTING = True
    DEBUG = True


config_dict = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}
