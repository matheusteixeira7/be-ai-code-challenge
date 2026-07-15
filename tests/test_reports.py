import time

import pytest
from sqlalchemy import event

from flask_sqlite_app import db
from flask_sqlite_app.models import Account


@pytest.mark.display_name("Step 4 — The settings report aggregates settings usage across accounts")
def test_report_settings(app, client):
    # The seeded accounts already contribute:
    # Elaine: "lang:US ; theme:black", Herman: "lang:FR".
    response = client.post("/admin/accounts", json={
        "name": "report_user",
        "password": "pw",
        "settings": "lang:US ; theme:white"
    })
    assert response.status_code == 201

    response = client.get("/admin/reports/settings")
    assert response.status_code == 200
    report = response.get_json()
    assert report["lang:US"] == 2
    assert report["lang:FR"] == 1
    assert report["theme:black"] == 1
    assert report["theme:white"] == 1


@pytest.mark.display_name("Step 4 — The settings report stays fast with thousands of accounts")
def test_report_performance(app, client):
    # Seed 2,000 accounts on top of the 2 default ones (Elaine: lang:US,
    # Herman: lang:FR). Odd i -> lang:US, even i -> lang:FR: 1,000 each.
    with app.app_context():
        db.session.add_all(
            Account(
                name=f"perf_user_{i}",
                password="pw",
                settings=f"lang:{'US' if i % 2 else 'FR'} ; theme:theme{i % 5}",
            )
            for i in range(2000)
        )
        db.session.commit()
        engine = db.engine

    select_statements = []

    def track_selects(conn, cursor, statement, parameters, context, executemany):
        if statement.lstrip().upper().startswith("SELECT"):
            select_statements.append(statement)

    event.listen(engine, "before_cursor_execute", track_selects)
    try:
        start = time.perf_counter()
        response = client.get("/admin/reports/settings")
        elapsed = time.perf_counter() - start
    finally:
        event.remove(engine, "before_cursor_execute", track_selects)

    assert response.status_code == 200
    report = response.get_json()
    assert report["lang:US"] == 1001
    assert report["lang:FR"] == 1001

    # Query budget for the report endpoint.
    assert len(select_statements) <= 5
    # Safety belt: generous wall-time bound.
    assert elapsed < 2.0
