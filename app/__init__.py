from flask import Flask, jsonify

from config import Config
from app.extensions import db, login_manager, migrate


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    @app.get("/health")
    def health():
        return jsonify({"status": "ok", "application": "Uber 2", "version": "2.0.0"})

    return app
