from flask import Blueprint, jsonify

from .. import db
from ..models import Account
from ..services.settings_parser import parse_settings

reports_bp = Blueprint("reports", __name__, url_prefix="/admin/reports")


@reports_bp.route("/settings", methods=["GET"])
def settings_report():
    account_ids = [row[0] for row in db.session.query(Account.id).all()]
    counts = {}
    for account_id in account_ids:
        account = db.session.get(Account, account_id)
        for key, value in parse_settings(account.settings):
            label = f"{key}:{value}"
            counts[label] = counts.get(label, 0) + 1
    return jsonify(counts)
