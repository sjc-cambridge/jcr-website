"""Unit test file for yourjcr routes
Simple checks whether the pages can be rendered correctly"""
from mock import patch


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
    response = client.get("/yourjcr/contact")
    assert response.status_code == 200


def test_constitution(client):
    """When trying to access this resource redirected to raven login"""
    response = client.get("/yourjcr/constitution")
    assert response.status_code == 303


def test_minutes(client):
    """Redirected to raven"""
    response = client.get("/yourjcr/minutes")
    assert response.status_code == 303


"""
@patch("website.views.yourjcr.johnian_access", side_effect=lambda: True)
def test_constitution_authenticated(johnian_access_patch, client):
    response = client.get("/yourjcr/constitution")
    assert response.status_code == 200
"""