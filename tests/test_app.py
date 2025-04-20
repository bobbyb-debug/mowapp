from app import create_app

def test_home_page():
    app = create_app()
    app.testing = True
    client = app.test_client()

    response = client.get('/')
    assert response.status_code == 200
