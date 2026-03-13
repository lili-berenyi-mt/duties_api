from backend.app import create_app
from backend.models import db
import pytest

@pytest.fixture
def client():
    app = create_app(config_name="testing")
    app.config['RATELIMIT_ENABLED'] = True
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all() 

def test_rate_limiting_spiking(client):
    for _ in range(12):
        client.get('/duties')
        
    response = client.get('/duties')
    assert response.status_code == 429