import pytest
from app import app

# https://flask.palletsprojects.com/en/stable/testing/#fixtures

@pytest.fixture()
def client_app():
    app.testing = True
    with app.test_client() as client_app:
        yield client_app

@pytest.fixture()
def runner():
    return app.test_cli_runner()