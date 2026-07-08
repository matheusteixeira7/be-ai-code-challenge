from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(test_config=None):
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    if test_config:
        app.config.update(test_config)
    db.init_app(app)

    from .models import Account  # noqa: F401 — registers the model with db
    from .seed import seed_default_accounts
    from .routes import home_bp
    from .routes.admin import admin_bp
    from .routes.reports import reports_bp

    with app.app_context():
        db.create_all()
        seed_default_accounts()

    app.register_blueprint(home_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(reports_bp)

    return app
