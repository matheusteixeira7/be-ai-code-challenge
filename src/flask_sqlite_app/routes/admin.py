from flask import Blueprint, request, jsonify

from ..services import accounts as account_service

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/accounts", methods=["POST"])
def add_account():
    name = request.json.get("name")
    password = request.json.get("password")
    settings = request.json.get("settings")
    if not name or not password:
        return jsonify({"error": "Name and password are required"}), 400
    acc = account_service.create_account(name, password, settings)
    return jsonify({"id": acc.id, "name": acc.name}), 201


@admin_bp.route("/accounts/<string:acc_id>", methods=["DELETE"])
def delete_account(acc_id):
    if not account_service.account_exists(acc_id):
        return jsonify({"error": "This account does not exist."}), 400
    account_service.delete_account(acc_id)
    return jsonify({"id": acc_id, "deleted": True}), 201


@admin_bp.route("/accounts", methods=["GET"])
def get_all_accounts():
    accounts = account_service.get_all_accounts()
    return jsonify(
        [
            {"id": a.id, "name": a.name, "settings": a.settings}
            for a in accounts
        ]
    )
