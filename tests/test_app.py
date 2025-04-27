# tests/test_app.py

def test_homepage_route(client):
    """Test the homepage route."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Dashboard" in response.data

def test_clients_page(client):
    """Test the clients page route."""
    response = client.get('/clients')
    assert response.status_code == 200
    assert b"Clients" in response.data  # Adjust depending on your page content

def test_404_page(client):
    """Test accessing an invalid page returns 404."""
    response = client.get('/nonexistentpage')
    assert response.status_code == 404
