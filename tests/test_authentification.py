import pytest
from flask_sqlite_app import create_app, db
from sqlalchemy import text
from random import randrange


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


@pytest.mark.display_name("Server health check")
def test_simple(app, client):
    response = client.get("/admin/accounts")
    assert response.status_code == 200


@pytest.mark.display_name("Register a new user, log in with that user, check the retrieved settings")
def test_register_and_login(app, client):
    # Register a user
    settings = "autotest_settings_" + str(randrange(1, 100))
    response = client.post("/admin/accounts", json={
        "name": "autotest_user",
        "password": "autotest_password",
        "settings": settings
    })
    assert response.status_code == 201

    # Login the user
    response = client.post("/login", json={
        "name": "autotest_user",
        "password": "autotest_password"
    })
    assert response.status_code == 200
    assert "token" in response.get_json()
    token = response.get_json()["token"]

    # Get settings
    response = client.get(
        "/settings",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.get_json()["settings"] == settings


@pytest.mark.display_name("The field in the DB was changed")
def test_db_field_size():
    import sqlite3
    import os
    conn = sqlite3.connect("src/instance/app.db")
    cursor = conn.execute("PRAGMA table_info(account)")
    found_password_field = False
    for row in cursor.fetchall():
        found_password_field = True
        if "password" in row:
            assert "VARCHAR(255)" in row
    assert found_password_field


@pytest.mark.display_name("The passwords are no more stored in clear text")
def test_password_storage(app, client):
    # Create a user.
    response = client.post("/admin/accounts", json={
        "name": "autotest_user_2",
        "password": "abcd1234",
        "settings": ""
    })
    assert response.status_code == 201
    new_user_id = response.get_json()["id"]
    assert isinstance(new_user_id, int)

    # Check the password is verified when login with the new user
    response = client.post("/login", json={
        "name": "autotest_user_2",
        "password": "abcd1234"
    })
    assert response.status_code == 200
    response = client.post("/login", json={
        "name": "autotest_user_2",
        "password": "bad password"
    })
    assert response.status_code != 200

    # Check how the password is stored in the db.
    with app.app_context():
        with db.engine.connect() as conn:
            query = f"SELECT password FROM account WHERE id = {new_user_id}"
            results = conn.execute(text(query)).fetchall()
            assert len(results) == 1
            assert results[0][0] != "abcd1234"
