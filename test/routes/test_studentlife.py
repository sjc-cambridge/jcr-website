"""Unit test file for studentlife routes
Simple checks whether the pages can be rendered correctly"""


def test_home(client):
    response = client.get("/studentlife")
    assert response.status_code == 308
    response = client.get("/studentlife/")
    assert response.status_code == 200
    response = client.get("/studentlife/home")
    assert response.status_code == 200


def test_404(client):
    response = client.get("/studentlife/does_not_exist")
    assert response.status_code == 404


def test_clubs_and_societies(client):
    response = client.get("/studentlife/clubsandsocieties")
    assert response.status_code == 200


def test_facilities(client):
    response = client.get("/studentlife/facilities")
    assert response.status_code == 200


def test_life_at_cambridge(client):
    response = client.get("/studentlife/atcambridge")
    assert response.status_code == 200
