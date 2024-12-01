import os

from flask import Flask

from flask_bootstrap import Bootstrap4

bootstrap = Bootstrap4()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY='dev')

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    bootstrap.init_app(app)

    from . import redirect
    app.register_blueprint(redirect.bp)

    return app
