from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()


def create_app(test_config=None):
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    if test_config:
        app.config.update(test_config)
    db.init_app(app)

    from .models import Account

    with app.app_context():
        db.create_all()
        nb_accounts = db.session.query(Account.id).count()
        if nb_accounts == 0:
            print("No accounts. We create two default accounts.")
            acc = Account(
                name="Elaine",
                password="abc",
                settings="lang:US ; theme:black"
            )
            db.session.add(acc)
            db.session.commit()
            acc = Account(
                name="Herman",
                password="123",
                settings="lang:FR"
            )
            db.session.add(acc)
            db.session.commit()

    @app.route("/", methods=["GET"])
    def home_page():
        return """
            Welcome to the "FutureTool Application".
            <br>
            You can try the url:
            <a href="/admin/accounts">
              /admin/accounts
            </a>
        """

    @app.route("/admin/accounts", methods=["POST"])
    def add_account():
        name = request.json.get("name")
        password = request.json.get("password")
        settings = request.json.get("settings")
        if not name or not password:
            return jsonify({"error": "Name and password are required"}), 400
        acc = Account(name=name, password=password, settings=settings)
        db.session.add(acc)
        db.session.commit()
        return jsonify({"id": acc.id, "name": acc.name}), 201

    @app.route("/admin/accounts/<string:acc_id>", methods=["DELETE"])
    def delete_account(acc_id):
        if Account.query.filter_by(id=acc_id).count():
            Account.query.filter_by(id=acc_id).delete()
            db.session.commit()
        else:
            return jsonify({"error": "This account does not exist."}), 400
        return jsonify({"id": acc_id, "deleted": True}), 201

    @app.route("/admin/accounts", methods=["GET"])
    def get_all_accounts():
        accounts = Account.query.all()
        return jsonify(
            [
                {"id": a.id, "name": a.name, "settings": a.settings}
                for a in accounts
            ]
        )

    return app
