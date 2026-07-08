import pytest


@pytest.mark.display_name("The settings report aggregates settings usage across accounts")
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
