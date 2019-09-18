"""Unit test file for protected committee section
Only checks you get the 303 redirect"""


def test_home(client):
    response = client.get("/committee")
    assert response.status_code == 303


def test_agenda(client):
    response = client.get("/committee/agenda")
    assert response.status_code == 303


def test_upload_minutes(client):
    response = client.get("/committee/upload_minutes")
    assert response.status_code == 303