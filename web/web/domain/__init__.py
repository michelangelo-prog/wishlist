# web/domain/__init__.py


import os

from flask import Flask, jsonify, make_response
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

MIGRATION_DIR = "migrations"

APP_SETTINGS = {
    "Development": "web.domain.config.DevelopmentConfig",
    "Test": "web.domain.config.TestingConfig",
    "Production": "web.domain.config.ProductionConfig",
}

# instantiate the extensions
db = SQLAlchemy()
migrate = Migrate()


def create_app(script_info=None):

    # instantiate the app
    app = Flask(__name__)

    # set config
    app_settings = os.getenv("APP_SETTINGS", "Production")
    app.config.from_object(APP_SETTINGS[app_settings])

    # set up extensions
    db.init_app(app)
    migrate.init_app(app, db, directory=MIGRATION_DIR)

    # register blueprints
    from web.domain.api.users import user_blueprint
    from web.domain.api.friendships import friendship_blueprint
    from web.domain.api.hello_world import helloworld_blueprint

    app.register_blueprint(user_blueprint, url_prefix="/api/v1/users")
    app.register_blueprint(friendship_blueprint, url_prefix="/api/v1/friendships")
    app.register_blueprint(helloworld_blueprint)

    # error handlers
    @app.errorhandler(400)
    def unauthorized_page(error):
        return make_response(jsonify({"error": "Bad Request"}), 400)

    @app.errorhandler(404)
    def page_not_found(error):
        return make_response(jsonify({"error": "Not found"}), 404)

    @app.errorhandler(500)
    def server_error_page(error):
        return make_response(jsonify({"error": "Internal Server Error"}), 500)

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}

    return app
