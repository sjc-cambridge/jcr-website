"""Important config file for pytest setup:
This defines several fixtures that can be accessed by any subsequent test
The most important one is the client fixture.
This exposes a test_client of the app to make any arbitrary http request to."""

import pytest
from website import create_site


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_site()
    yield app


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()


# TODO bypass authentication nicely
class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username="test", password="test"):
        return self._client.post(
            "/login", data={"username": username, "password": password}
        )

    def logout(self):
        return self._client.get("/logout")


@pytest.fixture
def auth(client):
    """Handles auth state"""
    return AuthActions(client)
