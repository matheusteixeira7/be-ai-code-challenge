import pytest
from flask_sqlite_app import create_app, db


def pytest_itemcollected(item):
    marker = item.get_closest_marker("display_name")
    if marker:
        item._nodeid = marker.args[0]


@pytest.fixture
def app():
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    }
    test_app = create_app(test_config)
    with test_app.app_context():
        db.create_all()
    return test_app


@pytest.fixture
def client(app):
    return app.test_client()
