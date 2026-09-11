from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config['JSON_SORT_KEYS'] = False

    from .routes import bp
    app.register_blueprint(bp)
    return app
