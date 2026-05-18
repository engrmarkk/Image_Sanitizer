from flask import Flask
from config import config_dict
from endpoints import main


def create_app(config_name="development"):
    app = Flask(__name__, template_folder="../templates", static_folder="static")

    app.config.from_object(config_dict[config_name])

    app.register_blueprint(main)
    return app
