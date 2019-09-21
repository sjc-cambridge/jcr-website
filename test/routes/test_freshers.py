"""Unit test file for freshers routes
Simple checks whether the pages can be rendered correctly"""


def test_home(client):
    response = client.get("/freshers")
    assert response.status_code == 308
    response = client.get("/freshers/")
    assert response.status_code == 200
    response = client.get("/freshers/home")
    assert response.status_code == 200


def test_404(client):
    response = client.get("/freshers/does_not_exist")
    assert response.status_code == 404


def test_vpwelcome(client):
    response = client.get("/freshers/vpwelcome")
    assert response.status_code == 200


def test_whattobring(client):
    response = client.get("/freshers/whattobring")
    assert response.status_code == 200


def test_yourfirstday(client):
    response = client.get("/freshers/yourfirstday")
    assert response.status_code == 200


def test_usefulcontacts(client):
    response = client.get("/freshers/usefulcontacts")
    assert response.status_code == 200


def test_glossary(client):
    response = client.get("/freshers/glossary")
    assert response.status_code == 200