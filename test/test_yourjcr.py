"""Unit test file for yourjcr routes
Simple checks whether the pages can be rendered correctly"""


def test_home(client):
    response = client.get("/yourjcr")
    assert response.status_code == 200


def test_committee(client):
    response = client.get("/yourjcr/committee")
    assert response.status_code == 200


def test_academic_affairs(client):
    response = client.get("/yourjcr/academicaffairs")
    assert response.status_code == 200


def test_access(client):
    response = client.get("/yourjcr/access")
    assert response.status_code == 200


def test_ethical(client):
    response = client.get("/yourjcr/committee/ethical")
    assert response.status_code == 200


def test_ents(client):
    response = client.get("/yourjcr/ents")
    assert response.status_code == 200


def test_contactus(client):
    response = client.get("/yourjcr/contactus")
    assert response.status_code == 200


def test_constitution(client):
    response = client.get("/yourjcr/constitution")
    assert response.status_code == 200


def test_minutes(client):
    response = client.get("/yourjcr/minutes")
    assert response.status_code == 200