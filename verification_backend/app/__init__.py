from flask import Flask
from app import config
from .logging import configure_logging

def create_app():

    configure_logging()

    # Initialize app
    app = Flask(__name__, instance_relative_config=True)

    # Load config
    config.init_app(app)

    # Register blueprints
    register_blueprints(app)

    # @app.errorhandler(Exception)
    # def handle_exception(e):
    #     return (repr(e), 204)

    return app


def register_blueprints(app):

    from app.routes import bp
    app.register_blueprint(bp)
