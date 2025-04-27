# tests/test_app.py
import pytest
from app import create_app

@pytest.fixture
def app():
    """Fixture to create a Flask app instance for testing."""
    app = create_app()
    app.config.update({
        "TESTING": True,  # Enable testing mode
    })
    return app

@pytest.fixture
def client(app):
    """Fixture to create a test client for the app."""
    return app.test_client()

def test_homepage_route(client):
    """Test the homepage route."""
    response = client.get('/')
    assert response.status_code == 200  # Expecting the homepage to return 200 OK
    assert b"Dashboard" in response.data  # Adjust this to match expected content
