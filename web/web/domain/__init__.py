# web/domain/__init__.py


import os

from flask import Flask, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

MIGRATION_DIR = "migrations"

# instantiate the extensions
db = SQLAlchemy()
migrate = Migrate()


def create_app(script_info=None):

    # instantiate the app
    app = Flask(__name__)

    # set config
    app_settings = os.getenv(
        "APP_SETTINGS", "web.domain.config.ProductionConfig"
    )
    app.config.from_object(app_settings)

    # set up extensions
    db.init_app(app)
    migrate.init_app(app, db, directory=MIGRATION_DIR)

    # register blueprints
    from web.domain.api.views import blueprint as api_blueprint

    app.register_blueprint(api_blueprint)


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
