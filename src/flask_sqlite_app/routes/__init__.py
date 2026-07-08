from flask import Blueprint

home_bp = Blueprint("home", __name__)


@home_bp.route("/", methods=["GET"])
def home_page():
    return """
        Welcome to the "FutureTool Application".
        <br>
        You can try the url:
        <a href="/admin/accounts">
          /admin/accounts
        </a>
    """
