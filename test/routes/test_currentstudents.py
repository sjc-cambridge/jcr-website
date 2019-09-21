"""Unit test file for currentstudents routes
Simple checks whether the pages can be rendered correctly"""


def test_home(client):
    response = client.get("/currentstudents")
    assert response.status_code == 308
    response = client.get("/currentstudents/")
    assert response.status_code == 303
    response = client.get("/currentstudents/home")
    assert response.status_code == 303

# NB! johnian_access preferentially returns a 303
# def test_404(client):
#     response = client.get("/currentstudents/does_not_exist")
#     assert response.status_code == 404


def test_committee(client):
    response = client.get("/currentstudents/welfare")
    assert response.status_code == 303


def test_elections(client):
    response = client.get("/currentstudents/elections")
    assert response.status_code == 303


def test_feedback(client):
    response = client.get("/currentstudents/feedback")
    assert response.status_code == 303


def test_transparency(client):
    response = client.get("/currentstudents/transparency")
    assert response.status_code == 303