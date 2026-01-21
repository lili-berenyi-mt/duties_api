from app import app as flask_app
from models import db
import pytest 

@pytest.fixture
def client():
    with flask_app.app_context():
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        flask_app.config['TESTING'] = True
        
        db.create_all()
        yield flask_app.test_client()
        db.drop_all()  

def test_get_ksbs_returns_200(client):
    result = client.get('/ksbs')
    assert result.status_code == 200